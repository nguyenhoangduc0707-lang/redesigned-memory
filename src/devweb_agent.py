import argparse
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from src.config import ROOT_DIR


SENSITIVE_HEADER_NAMES = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-api-key",
    "x-auth-token",
    "proxy-authorization",
}
SENSITIVE_QUERY_KEYS = {"token", "access_token", "api_key", "key", "secret", "password", "session"}


def redact_value(value):
    if value is None:
        return None
    text = str(value)
    if len(text) <= 4:
        return "***"
    return f"{text[:2]}***{text[-2:]}"


def redact_headers(headers):
    safe = {}
    for name, value in (headers or {}).items():
        if name.lower() in SENSITIVE_HEADER_NAMES:
            safe[name] = "<REDACTED>"
        else:
            safe[name] = value
    return safe


def redact_url(url):
    parsed = urlparse(url)
    if not parsed.query:
        return url

    pairs = []
    for part in parsed.query.split("&"):
        if "=" not in part:
            pairs.append(part)
            continue
        key, value = part.split("=", 1)
        if key.lower() in SENSITIVE_QUERY_KEYS:
            pairs.append(f"{key}=<REDACTED>")
        else:
            pairs.append(f"{key}={value}")
    return parsed._replace(query="&".join(pairs)).geturl()


@dataclass
class DevWebEvent:
    type: str
    data: dict
    timestamp: float = field(default_factory=time.time)

    def as_dict(self):
        return {"type": self.type, "timestamp": self.timestamp, **self.data}


class DevWebReport:
    def __init__(self, url):
        self.url = url
        self.events = []
        self.summary = {}

    def add(self, event_type, **data):
        self.events.append(DevWebEvent(event_type, data))

    def as_dict(self):
        return {
            "url": self.url,
            "summary": self.summary,
            "events": [event.as_dict() for event in self.events],
        }

    def write(self, output_dir):
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        json_path = output_dir / f"devweb_report_{stamp}.json"
        md_path = output_dir / f"devweb_report_{stamp}.md"
        json_path.write_text(json.dumps(self.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        md_path.write_text(self.to_markdown(), encoding="utf-8")
        return json_path, md_path

    def to_markdown(self):
        lines = [
            "# DevWeb F12 Report",
            "",
            f"- URL: `{self.url}`",
            f"- Events: {len(self.events)}",
            "",
            "## Summary",
        ]
        for key, value in self.summary.items():
            lines.append(f"- {key}: `{value}`")

        lines.extend(["", "## Findings"])
        for event in self.events:
            if event.type in ("console", "page_error", "request_failed", "response_error"):
                payload = event.as_dict()
                lines.append(f"- **{event.type}**: `{payload}`")

        lines.extend(["", "## Inventory"])
        for event in self.events:
            if event.type in ("dom_inventory", "storage_inventory", "performance"):
                lines.append(f"### {event.type}")
                lines.append("```json")
                lines.append(json.dumps(event.data, ensure_ascii=False, indent=2))
                lines.append("```")
        return "\n".join(lines) + "\n"


class DevWebAgent:
    def __init__(self, headless=True, output_dir=None):
        self.headless = headless
        self.output_dir = Path(output_dir or ROOT_DIR / "reports" / "devweb")

    def audit(self, url, actions=None, wait_ms=1000, screenshot=True):
        from playwright.sync_api import sync_playwright

        report = DevWebReport(url)
        actions = actions or []

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=self.headless)
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()

            self._wire_events(page, report)
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(wait_ms)

            for action in actions:
                self._run_action(page, action, report)

            report.add("dom_inventory", **self._dom_inventory(page))
            report.add("storage_inventory", **self._storage_inventory(page, context))
            report.add("performance", **self._performance(page))

            if screenshot:
                screenshot_path = self.output_dir / f"devweb_{time.strftime('%Y%m%d_%H%M%S')}.png"
                screenshot_path.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(screenshot_path), full_page=True)
                report.add("screenshot", path=str(screenshot_path))

            report.summary = self._summarize(report)
            context.close()
            browser.close()

        return report

    def _wire_events(self, page, report):
        page.on("console", lambda msg: report.add("console", level=msg.type, text=msg.text))
        page.on("pageerror", lambda exc: report.add("page_error", message=str(exc)))
        page.on("requestfailed", lambda request: report.add(
            "request_failed",
            url=redact_url(request.url),
            method=request.method,
            failure=request.failure,
        ))
        page.on("response", lambda response: self._record_response(response, report))
        page.on("request", lambda request: report.add(
            "request",
            url=redact_url(request.url),
            method=request.method,
            resource_type=request.resource_type,
            headers=redact_headers(request.headers),
        ))

    def _record_response(self, response, report):
        status = response.status
        event_type = "response_error" if status >= 400 else "response"
        report.add(
            event_type,
            url=redact_url(response.url),
            status=status,
            headers=redact_headers(response.headers),
        )

    def _run_action(self, page, action, report):
        kind = action.get("type")
        selector = action.get("selector")
        if kind == "click":
            page.click(selector)
        elif kind == "fill":
            page.fill(selector, action.get("value", ""))
        elif kind == "press":
            page.press(selector, action.get("key", "Enter"))
        elif kind == "wait":
            page.wait_for_timeout(int(action.get("ms", 1000)))
        elif kind == "goto":
            page.goto(action["url"], wait_until="domcontentloaded")
        else:
            raise ValueError(f"Unsupported action type: {kind}")
        report.add("action", action={**action, "value": redact_value(action.get("value")) if "value" in action else None})

    def _dom_inventory(self, page):
        return page.evaluate("""
            () => ({
                title: document.title,
                url: location.href,
                links: Array.from(document.links).slice(0, 100).map(a => ({text: a.innerText.trim().slice(0, 80), href: a.href})),
                buttons: Array.from(document.querySelectorAll('button,input[type=button],input[type=submit]')).slice(0, 100).map(b => ({
                    text: (b.innerText || b.value || '').trim().slice(0, 80),
                    disabled: !!b.disabled
                })),
                forms: Array.from(document.forms).slice(0, 50).map(f => ({
                    action: f.action,
                    method: f.method,
                    fields: Array.from(f.elements).map(e => ({name: e.name, type: e.type, required: !!e.required}))
                })),
                images: document.images.length,
                scripts: document.scripts.length,
                stylesheets: document.styleSheets.length
            })
        """)

    def _storage_inventory(self, page, context):
        storage = page.evaluate("""
            () => ({
                localStorageKeys: Object.keys(localStorage || {}),
                sessionStorageKeys: Object.keys(sessionStorage || {})
            })
        """)
        cookies = context.cookies()
        storage["cookies"] = [{"name": cookie.get("name"), "domain": cookie.get("domain")} for cookie in cookies]
        return storage

    def _performance(self, page):
        return page.evaluate("""
            () => {
                const nav = performance.getEntriesByType('navigation')[0];
                const resources = performance.getEntriesByType('resource');
                return {
                    domContentLoadedMs: nav ? Math.round(nav.domContentLoadedEventEnd) : null,
                    loadEventMs: nav ? Math.round(nav.loadEventEnd) : null,
                    resourceCount: resources.length,
                    slowResources: resources
                        .filter(r => r.duration > 1000)
                        .slice(0, 20)
                        .map(r => ({name: r.name, durationMs: Math.round(r.duration), type: r.initiatorType}))
                };
            }
        """)

    def _summarize(self, report):
        events = report.events
        return {
            "console_messages": sum(1 for event in events if event.type == "console"),
            "page_errors": sum(1 for event in events if event.type == "page_error"),
            "failed_requests": sum(1 for event in events if event.type == "request_failed"),
            "http_errors": sum(1 for event in events if event.type == "response_error"),
        }


def load_actions(path):
    if not path:
        return []
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv=None):
    parser = argparse.ArgumentParser(description="DevWeb F12 Agent")
    parser.add_argument("url", help="URL to audit")
    parser.add_argument("--actions", help="JSON file with interaction actions")
    parser.add_argument("--headed", action="store_true", help="Show browser window")
    parser.add_argument("--wait-ms", type=int, default=1000)
    parser.add_argument("--no-screenshot", action="store_true")
    parser.add_argument("--output-dir", default=str(ROOT_DIR / "reports" / "devweb"))
    args = parser.parse_args(argv)

    agent = DevWebAgent(headless=not args.headed, output_dir=args.output_dir)
    report = agent.audit(
        args.url,
        actions=load_actions(args.actions),
        wait_ms=args.wait_ms,
        screenshot=not args.no_screenshot,
    )
    json_path, md_path = report.write(args.output_dir)
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")


if __name__ == "__main__":
    main()

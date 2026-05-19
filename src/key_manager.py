import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

from src.config import ENV_PATH


PLACEHOLDER_MARKERS = (
    "your_",
    "change-this",
    "changeme",
    "placeholder",
    "example",
    "test",
    "dummy",
    "fake",
)

KEY_GROUPS = {
    "facebook": ("FACEBOOK_PAGE_ACCESS_TOKEN", "FACEBOOK_ACCESS_TOKEN", "FACEBOOK_PAGE_ID"),
    "tiktok": ("TIKTOK_ACCESS_TOKEN", "TIKTOK_BUSINESS_ID", "APIFY_API_TOKEN"),
    "zalo": ("ZALO_ACCESS_TOKEN", "ZALO_OA_ID"),
    "shopee": ("SHOPEE_PARTNER_ID", "SHOPEE_SHOP_ID", "SHOPEE_API_KEY"),
    "notebooklm": ("NOTEBOOKLM_NOTEBOOK_ID",),
    "ai": ("DEEPSEEK_API_KEY", "OPENAI_API_KEY", "GEMINI_API_KEY"),
}


@dataclass
class KeyRecord:
    name: str
    group: str
    status: str
    length: int
    reason: str

    def as_dict(self):
        return {
            "name": self.name,
            "group": self.group,
            "status": self.status,
            "length": self.length,
            "reason": self.reason,
        }


def load_env_values(env_path: Path = ENV_PATH):
    values = {}
    if env_path.exists():
        values.update({k: v for k, v in dotenv_values(env_path).items() if k})
    for key, value in os.environ.items():
        values.setdefault(key, value)
    return values


def classify_value(name, value):
    if value is None or str(value).strip() == "":
        return "missing", "empty"

    normalized = str(value).strip().lower()
    if any(marker in normalized for marker in PLACEHOLDER_MARKERS):
        return "placeholder", "matches placeholder marker"

    if name.endswith("_ID") and len(str(value).strip()) >= 6:
        return "present", "id-like value present"

    if any(token in name for token in ("KEY", "TOKEN", "SECRET")):
        if len(str(value).strip()) < 20:
            return "suspicious", "secret-like value is short"
        return "present", "secret-like value present"

    return "present", "value present"


def audit_keys(env_path: Path = ENV_PATH):
    values = load_env_values(env_path)
    records = []
    seen = set()

    for group, names in KEY_GROUPS.items():
        for name in names:
            value = values.get(name)
            status, reason = classify_value(name, value)
            records.append(KeyRecord(name, group, status, len(value or ""), reason))
            seen.add(name)

    for name, value in values.items():
        if name in seen:
            continue
        if any(token in name for token in ("KEY", "TOKEN", "SECRET", "PASSWORD")):
            status, reason = classify_value(name, value)
            records.append(KeyRecord(name, "unmapped", status, len(value or ""), reason))

    return records


def get_key(name, default=None):
    values = load_env_values()
    value = values.get(name, default)
    status, _ = classify_value(name, value)
    if status in ("missing", "placeholder"):
        return default
    return value

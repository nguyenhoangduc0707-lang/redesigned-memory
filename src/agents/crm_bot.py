from dataclasses import dataclass

from src.agents import Agent


@dataclass
class CustomerMessage:
    platform: str
    user_id: str
    text: str
    context: dict | None = None


class CRMBot:
    def __init__(self, agent=None):
        self.agent = agent or Agent("CRM Bot")

    def draft_reply(self, message: CustomerMessage):
        prompt = (
            "Draft a short Vietnamese customer-service reply for affiliate commerce.\n"
            f"Platform: {message.platform}\n"
            f"Customer: {message.user_id}\n"
            f"Message: {message.text}\n"
            "Rules: be polite, concise, do not invent order status, ask for missing info if needed."
        )
        result = self.agent.run(prompt)
        return {
            "platform": message.platform,
            "user_id": message.user_id,
            "status": result.get("status"),
            "source": result.get("source"),
            "reply": result.get("answer") or "Cam on ban. Vui long cung cap them thong tin de minh ho tro nhanh hon.",
            "error": result.get("error"),
        }


def draft_reply(platform, user_id, text, context=None):
    return CRMBot().draft_reply(CustomerMessage(platform, user_id, text, context))

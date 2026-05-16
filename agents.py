# agents_unified.py
import os

USE_EMOJI = os.getenv('USE_EMOJI', 'True').lower() == 'true'

def get_agent_response(prompt):
    if USE_EMOJI:
        # Nội dung từ agents.py (có emoji)
        return f"🤖 Agent response: {prompt}"
    else:
        # Nội dung từ agents_no_emoji.py (không emoji)
        return f"Agent response: {prompt}"

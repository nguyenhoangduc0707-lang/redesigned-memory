import os

AI_IDENTITY = "SEN Kernel V3 - AI OS"
FOUNDER_INFO = "SEN Dev"
DEDICATION = "Tối ưu đa chiều, tuân thủ Meta Policy"

DEBUG = True
API_TIMEOUT = 30
DB_PATH = 'ai_os.db'

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT_DIR, '.env')

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
EXTERNAL_LLM_PROVIDER = os.getenv("EXTERNAL_LLM_PROVIDER", "openai")

LOCAL_LLM_COMMAND = os.getenv("LOCAL_LLM_COMMAND", "ollama run llama3")
LOCAL_LLM_TIMEOUT = int(os.getenv("LOCAL_LLM_TIMEOUT", "60"))
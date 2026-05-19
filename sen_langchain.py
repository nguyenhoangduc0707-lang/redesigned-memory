# sen_langchain.py
import os
import subprocess
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Module tự viết
from notebooklm_client import NotebookLMClient

DEEPSEEK_API_KEY = "sk-1fcf05ca46e64675adb29ba78c05e595"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
NOTEBOOK_ID = os.environ.get("NOTEBOOKLM_NOTEBOOK_ID", "7f173758-e23c-4fbd-814d-0bd9c5391c74")

# Khởi tạo model
llm = ChatOpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
    model="deepseek-chat",
    temperature=0.2,
)

# Tool PowerShell
@tool
def execute_powershell(command: str) -> str:
    """Thực thi lệnh PowerShell và trả về kết quả."""
    try:
        result = subprocess.run(
            ["powershell.exe", "-Command", command],
            capture_output=True, text=True, shell=True, timeout=30
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Lỗi: {e}"

# Tool NotebookLM
notebook_client = NotebookLMClient(NOTEBOOK_ID)

@tool
def ask_notebook(question: str) -> str:
    """Hỏi NotebookLM về dự án, trả về câu trả lời."""
    result = notebook_client.ask(question)
    if result["answer"]:
        return result["answer"]
    else:
        return f"Lỗi NotebookLM: {result['error']}"

tools = [execute_powershell, ask_notebook]

# Tạo agent với prompt
prompt = PromptTemplate.from_template("""
Bạn là trợ lý AI tên SEN, chuyên về dự án AI_OS_KERNEL_V3.
Bạn có hai công cụ:
- execute_powershell: để chạy lệnh PowerShell khi người dùng yêu cầu thực hiện tác vụ.
- ask_notebook: để tra cứu thông tin về dự án (kiến trúc, module, xử lý video, v.v.)

Hãy sử dụng công cụ phù hợp.
Nếu người dùng hỏi về code/lệnh/thực thi, hãy dùng execute_powershell.
Nếu hỏi về kiến thức dự án, hãy dùng ask_notebook.

Lịch sử hội thoại:
{chat_history}
Câu hỏi: {input}
{agent_scratchpad}
""")

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Chạy tương tác
if __name__ == "__main__":
    print("SEN - AI (DeepSeek + NotebookLM) sẵn sàng. Gõ 'exit' thoát.")
    history = []
    while True:
        q = input("\nBạn: ")
        if q.lower() in ("exit", "quit"):
            break
        response = agent_executor.invoke({"input": q, "chat_history": "\n".join(history)})
        answer = response["output"]
        print(f"SEN: {answer}")
        history.append(f"Bạn: {q}\nSEN: {answer}")
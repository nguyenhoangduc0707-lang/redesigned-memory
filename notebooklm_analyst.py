import subprocess
import json
import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

NOTEBOOK_ID = os.environ.get("NOTEBOOKLM_NOTEBOOK_ID", "7f173758-e23c-4fbd-814d-0bd9c5391c74")

def ask_notebook(question):
    cmd = ['nlm', 'notebook', 'query', NOTEBOOK_ID, question, '--json']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=60)
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            return data.get('value', {}).get('answer', 'No answer from NotebookLM')
        return f"Lỗi: {result.stderr}"
    except Exception as e:
        return f"Lỗi: {e}"

def generate_daily_report():
    conn = sqlite3.connect('ai_os.db')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    query = f"SELECT * FROM campaign_metrics WHERE date(timestamp) = '{yesterday}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    if df.empty:
        report_text = f"Không có dữ liệu cho ngày {yesterday}."
    else:
        report_text = df.to_string()
    question = f"Phân tích hiệu suất chiến dịch affiliate dựa trên dữ liệu ngày {yesterday}:\n{report_text}\nưa ra đề xuất cải tiến chiến dịch affiliate."
    return ask_notebook(question)

if __name__ == "__main__":
    report = generate_daily_report()
    with open('daily_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print("Daily report saved.")
    print(report)

import json
from pathlib import Path
import re
from collections import Counter

DATA_DIR = Path("data/knowledge")

def load_all_knowledge():
    """Đọc tất cả file JSON, trả về list các dict với content, summary, topics"""
    docs = []
    for json_file in DATA_DIR.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            text = data['summary'] + " " + " ".join(data['key_points'])
            docs.append({
                'id': json_file.stem,
                'text': text,
                'summary': data['summary'],
                'topics': data['topics']
            })
        except Exception as e:
            print(f"Lỗi đọc {json_file}: {e}")
    return docs

def search(query, docs, top_k=2):
    """Tìm kiếm dựa trên số lần xuất hiện từ khóa"""
    # Tách từ khóa, loại bỏ stopwords cơ bản
    query_words = set(re.findall(r'\b\w+\b', query.lower()))
    stopwords = {'của', 'và', 'là', 'có', 'được', 'với', 'một', 'các', 'những', 'để', 'cho', 'về', 'như', 'khi', 'không', 'cũng', 'thì', 'bị', 'do', 'tại', 'theo', 'trên', 'dưới', 'vào', 'ra', 'lên', 'xuống'}
    query_words = {w for w in query_words if w not in stopwords and len(w) > 2}
    
    results = []
    for doc in docs:
        doc_words = re.findall(r'\b\w+\b', doc['text'].lower())
        word_count = Counter(doc_words)
        score = sum(word_count.get(w, 0) for w in query_words)
        if score > 0:
            results.append((score, doc))
    results.sort(reverse=True, key=lambda x: x[0])
    return [doc for score, doc in results[:top_k]]

if __name__ == "__main__":
    docs = load_all_knowledge()
    print(f"Đã tải {len(docs)} tài liệu.")
    while True:
        q = input("Câu hỏi (hoặc 'exit'): ").strip()
        if q.lower() == 'exit':
            break
        found = search(q, docs)
        if found:
            for i, doc in enumerate(found):
                print(f"\n--- Kết quả {i+1} ---")
                print(f"Chủ đề: {', '.join(doc['topics'])}")
                print(f"Tóm tắt: {doc['summary'][:300]}")
        else:
            print("Không tìm thấy tri thức liên quan.")
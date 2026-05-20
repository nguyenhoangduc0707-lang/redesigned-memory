import json
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

DATA_DIR = Path("data/knowledge")
CHROMA_DIR = Path("data/embeddings/chroma")
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

print("Đang khởi tạo embedding function...")
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
print("✅ Đã tải mô hình embedding.")

client = chromadb.PersistentClient(path=str(CHROMA_DIR))

# Xóa collection cũ
try:
    client.delete_collection("sen_knowledge")
    print("✅ Đã xóa collection cũ.")
except:
    pass

# Tạo collection mới
collection = client.create_collection(name="sen_knowledge", embedding_function=ef)
print("✅ Đã tạo collection mới.")

def add_knowledge_to_db(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    text_to_embed = data['summary'] + "\n" + "\n".join(data['key_points'])
    doc_id = json_path.stem
    collection.upsert(
        ids=[doc_id],
        metadatas=[{
            "source": str(json_path),
            "summary": data['summary'],
            "topics": ", ".join(data['topics'])
        }],
        documents=[text_to_embed]
    )
    print(f"✅ Đã thêm {doc_id}")

def add_all_json_files():
    json_files = list(DATA_DIR.glob("*.json"))
    if not json_files:
        print("⚠️ Không có file JSON nào trong data/knowledge")
        return
    print(f"Tìm thấy {len(json_files)} file JSON trong data/knowledge")
    for json_file in json_files:
        add_knowledge_to_db(json_file)
    print(f"✅ Đã thêm {len(json_files)} file vào vector DB")

if __name__ == "__main__":
    print("=== XÂY DỰNG VECTOR DB ===")
    add_all_json_files()
    print(f"Số lượng tài liệu trong DB: {collection.count()}")
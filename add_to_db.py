import json
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

DATA_DIR = Path("data/knowledge")
CHROMA_DIR = Path("data/embeddings/chroma")
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

print("Loading embedding model...")
ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=str(CHROMA_DIR))

# Xóa collection cũ nếu có
try:
    client.delete_collection("sen_knowledge")
    print("Deleted old collection")
except Exception as e:
    print(f"No old collection or error: {e}")

# Tạo collection mới
try:
    collection = client.create_collection(name="sen_knowledge", embedding_function=ef)
    print("Created new collection")
except Exception as e:
    print(f"Error creating collection: {e}")
    exit()

# Đọc file JSON
json_file = DATA_DIR / "1000000448.json"
try:
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f"Error reading JSON: {e}")
    exit()

text_to_embed = data['summary'] + "\n" + "\n".join(data['key_points'])
doc_id = json_file.stem
print(f"Upserting {doc_id}...")
try:
    collection.upsert(
        ids=[doc_id],
        metadatas=[{
            "source": str(json_file),
            "summary": data['summary'],
            "topics": ", ".join(data['topics'])
        }],
        documents=[text_to_embed]
    )
    print(f"Success! Collection now has {collection.count()} documents.")
except Exception as e:
    print(f"Upsert error: {e}")
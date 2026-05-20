import chromadb
client = chromadb.PersistentClient(path='data/embeddings/chroma')
print("Collections:", [c.name for c in client.list_collections()])
if 'sen_knowledge' in [c.name for c in client.list_collections()]:
    col = client.get_collection('sen_knowledge')
    print("Count:", col.count())
else:
    print("Collection not found")

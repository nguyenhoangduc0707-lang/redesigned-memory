from sentence_transformers import SentenceTransformer, util

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('microsoft/codebert-base')
    return _model

def semantic_similarity(original: str, improved: str) -> float:
    model = get_model()
    emb1 = model.encode(original, convert_to_tensor=True)
    emb2 = model.encode(improved, convert_to_tensor=True)
    return util.pytorch_cos_sim(emb1, emb2).item()

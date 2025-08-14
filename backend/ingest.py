import os, math
from typing import List
from sentence_transformers import SentenceTransformer
import openai
import tiktoken

# Simple chunking by characters (can be improved using sentence/semantic chunking)
def chunk_text(text: str, max_chars: int = 1000):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end
    return chunks

def load_texts_from_dir(dir_path):
    texts = []
    for fname in os.listdir(dir_path):
        full = os.path.join(dir_path, fname)
        if os.path.isfile(full) and fname.lower().endswith(('.txt', '.md')):
            with open(full, 'r', encoding='utf-8') as f:
                texts.append({'source': fname, 'text': f.read()})
    return texts

def get_openai_embedding(texts, model='text-embedding-3-small', openai_api_key=None):
    if openai_api_key:
        openai.api_key = openai_api_key
    resp = openai.Embedding.create(model=model, input=texts)
    embeddings = [r['embedding'] for r in resp['data']]
    return embeddings

def get_local_embeddings(texts, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embs = model.encode(texts, show_progress_bar=False)
    return embs.tolist()

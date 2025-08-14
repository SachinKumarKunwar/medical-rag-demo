import argparse, os, uuid
from ingest import load_texts_from_dir, chunk_text, get_local_embeddings, get_openai_embedding
import chromadb
from chromadb.config import Settings
import math
from dotenv import load_dotenv
import json
load_dotenv()

def main(docs_dir, persist_dir='./chroma_db', use_openai=False):
    texts = load_texts_from_dir(docs_dir)
    print(f'Found {len(texts)} documents')
    all_chunks = []
    for doc in texts:
        chunks = chunk_text(doc['text'], max_chars=800)
        for i,c in enumerate(chunks):
            all_chunks.append({'id': f"{doc['source']}_{i}", 'text': c, 'meta': {'source': doc['source'], 'chunk': i}})

    print(f'Created {len(all_chunks)} chunks')
    docs = [c['text'] for c in all_chunks]
    ids = [c['id'] for c in all_chunks]
    metas = [c['meta'] for c in all_chunks]

    embeddings = None
    if use_openai:
        from dotenv import get_key
        import os
        from ingest import get_openai_embedding
        key = os.getenv('OPENAI_API_KEY')
        embeddings = get_openai_embedding(docs, openai_api_key=key)
    else:
        embeddings = get_local_embeddings(docs)

    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_dir))
    collection = None
    try:
        collection = client.get_collection('medical')
    except Exception:
        collection = client.create_collection('medical')

    # add into collection
    collection.add(ids=ids, documents=docs, metadatas=metas, embeddings=embeddings)
    print('Added to Chroma collection. Persist directory:', persist_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--docs_dir', default='sample_data/papers')
    parser.add_argument('--persist_dir', default='./chroma_db')
    parser.add_argument('--use_openai', action='store_true', help='Use OpenAI embeddings if set')
    args = parser.parse_args()
    main(args.docs_dir, args.persist_dir, use_openai=args.use_openai)

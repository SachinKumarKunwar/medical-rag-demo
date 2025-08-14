---
title: Medical RAG Demo
emoji: 🩺
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.25.0"
app_file: streamlit_app.py
pinned: false
---
# Medical Literature RAG for Healthcare Professionals

**What this repo contains**
- A reproducible RAG (Retrieval-Augmented Generation) demonstration tailored for medical literature + anonymized patient data.
- Ingestion scripts to chunk and embed medical texts (PDFs / text).
- A lightweight vector store using Chroma (or FAISS) to store embeddings.
- A Streamlit demo app that queries the vector store and generates evidence-backed answers (via OpenAI; fallback to sentence-transformers embeddings).
- Sample synthetic/anonymized patient data and short example clinical guideline text.
- Dockerfile and CI/CD workflow stub for deployment.

**Important**
- This project prepares everything **locally**. I cannot push to GitHub or actually deploy to a remote hosting provider from this environment. However, the repository includes deployment instructions and CI stubs so you can push & deploy with a single click when you run it locally.
- You will need an OpenAI API key to use the OpenAI embedding + generation features. The code falls back to `sentence-transformers` embeddings if no key is present.

## Quickstart (local)
1. Unzip the project and `cd` into it.
2. Create a Python virtual environment and install requirements:
```bash
python -m venv .venv
source .venv/bin/activate    # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```
3. Fill `.env` (or set environment variables):
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o            # or a model available to you (set or leave blank to use local fallback behaviour)
EMBEDDING_MODEL=openai-text-embedding-3-small
```
4. Ingest the sample documents to create the Chroma DB:
```bash
python scripts/create_embeddings.py --docs_dir sample_data/papers --persist_dir ./chroma_db
```
5. Run the Streamlit demo:
```bash
streamlit run app/streamlit_app.py
```

## Files of interest
- `scripts/create_embeddings.py` — ingest and build vector DB from `sample_data/papers`.
- `backend/ingest.py` — helper functions for chunking and embedding.
- `backend/retrieval.py` — retrieval and answer generation logic.
- `app/streamlit_app.py` — demo UI.
- `utils/drug_interactions.py` — small example drug-interaction checker.
- `sample_data/` — synthetic guideline text and anonymized patient CSV.

## Deployment notes
- The repo includes a GitHub Actions workflow stub `.github/workflows/deploy.yml` that can be adapted to deploy to HuggingFace Spaces or a cloud VM.
- The Dockerfile builds a container that serves the Streamlit app; you can push that image to Docker Hub and connect to a cloud host.

## Security & Compliance
- **Do not** load any real patient data until you are sure your runtime and deployment targets are HIPAA/GDPR compliant.
- The `sample_data/patients.csv` is synthetic and anonymized and intended only for testing.

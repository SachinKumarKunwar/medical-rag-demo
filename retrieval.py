import os
import chromadb
from chromadb.config import Settings
from typing import List
import openai
from drug_interactions import check_interactions
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

PERSIST_DIR = os.getenv('PERSIST_DIR', './chroma_db')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')

# Connect to Chroma (local)
def get_client(persist_directory=PERSIST_DIR):
    # in-memory by default; set persist_directory to persist to disk
    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_directory))
    return client

def retrieve_docs(query: str, n_docs:int=4):
    client = get_client()
    try:
        col = client.get_collection("medical")
    except Exception:
        return []
    results = col.query(query_texts=[query], n_results=n_docs)
    # results contains 'documents' and 'metadatas'
    docs = []
    docs_list = results.get('documents', [[]])[0]
    metas = results.get('metadatas', [[]])[0]
    for d, m in zip(docs_list, metas):
        docs.append({'text': d, 'meta': m})
    return docs

def generate_answer(query: str, patient_record: dict=None, top_k:int=4):
    docs = retrieve_docs(query, n_docs=top_k)
    # Build context
    context_sections = []
    for i, d in enumerate(docs):
        source = d['meta'].get('source', f'doc{i}')
        context_sections.append(f"Source: {source}\nText: {d['text']}")
    patient_section = ''
    warnings = []
    if patient_record is not None:
        patient_section = f"""Patient:
ID: {patient_record.get('patient_id')}
Age: {patient_record.get('age')}
Sex: {patient_record.get('sex')}
Medications: {patient_record.get('medications')}
Allergies: {patient_record.get('allergies')}
Conditions: {patient_record.get('conditions')}
"""
        meds = [m.strip() for m in str(patient_record.get('medications','')).split(';') if m.strip()]
        warnings = check_interactions(meds)

    prompt = f"""You are a helpful clinical assistant. Use the evidence below to answer the clinician's question.
Question: {query}

Patient info:
{patient_section}

Evidence (top {top_k}):
{chr(10).join(context_sections)}

Instructions: Answer succinctly. Provide a recommendation and cite the sources (name the source file). If patient-specific risks exist (e.g., drug interactions), state them clearly and suggest alternatives or monitoring. If you are uncertain, say so and recommend confirmatory checks.
"""

    # Call OpenAI ChatCompletion (if key present)
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
        messages = [
            {'role':'system','content':'You are a medical assistant that cites sources.'},
            {'role':'user','content': prompt}
        ]
        resp = openai.ChatCompletion.create(model=OPENAI_MODEL, messages=messages, temperature=0.0, max_tokens=500)
        answer = resp['choices'][0]['message']['content']
    else:
        answer = """[OPENAI_API_KEY not set] Preview answer: Use the retrieved evidence to craft an answer.\n\n"""
        answer += "\n\n".join([f"Source: {d['meta'].get('source','unknown')} -- excerpt: {d['text'][:300]}" for d in docs])

    return {'answer': answer, 'evidence': docs, 'warnings': warnings}

def load_patient_by_id(patient_id, path='sample_data/patients.csv'):
    df = pd.read_csv(path)
    rec = df[df['patient_id']==patient_id]
    if rec.empty:
        return None
    row = rec.iloc[0].to_dict()
    return row

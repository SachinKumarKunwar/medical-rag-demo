import streamlit as st
from retrieval import generate_answer, load_patient_by_id
import os

st.set_page_config(page_title='Medical Literature RAG Demo', layout='wide')
st.title('Medical Literature RAG — Demo')

with st.sidebar:
    st.markdown('### Demo Controls')
    patient_id = st.selectbox('Select patient (sample)', options=['P001','P002','P003'])
    top_k = st.slider('Number of retrieved documents', 1, 6, 4)
    run_button = st.button('Get Answer')

st.markdown('Enter a clinical question (e.g., "Recommended lisinopril dose for elderly with CKD?")')
query = st.text_area('Question', height=120, value='What is the recommended dose of lisinopril for an elderly patient?')

if run_button:
    st.info('Running retrieval + generation...')
    patient = load_patient_by_id(patient_id)
    res = generate_answer(query, patient_record=patient, top_k=top_k)
    st.subheader('AI Answer (evidence-backed)')
    st.write(res['answer'])
    st.subheader('Retrieved Evidence')
    for ev in res['evidence']:
        st.markdown(f"**Source:** {ev['meta'].get('source','unknown')}")
        st.write(ev['text'][:800] + ('...' if len(ev['text'])>800 else ''))
    if res['warnings']:
        st.subheader('Safety / Interaction Warnings')
        for w in res['warnings']:
            st.error(f"{w['pair']} — {w['severity'].upper()} — {w['message']}")

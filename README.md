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

## Overview
This repository demonstrates a streamlined Retrieval-Augmented Generation (RAG) demo tailored for medical literature and anonymized patient data. It’s designed to help healthcare professionals quickly access evidence-based insights through an interactive app.

## What You’ll Find Here
- **RAG Workflow**: Document retrieval combined with AI for accurate, source-cited answers.  
- **Text Ingestion Tools**: Chunk and embed medical texts for indexing.  
- **Vector Storage**: Powered by Chroma (or FAISS) for storing embeddings.  
- **Interactive Frontend**: Built with Streamlit for intuitive querying.  
- **Sample Data**: Anonymized patient records and guideline text for testing.  
- **Deployment Templates**: Includes Dockerfile and GitHub Actions stub for streamlined deployment.

---

## Getting Started (Local Setup)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SachinKumarKunwar/medical-rag-demo.git
   cd medical-rag-demo

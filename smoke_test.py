# Quick smoke test to confirm imports
import sys
try:
    import streamlit
    import chromadb
    import openai
    import sentence_transformers
    print('Imports OK')
except Exception as e:
    print('Import error:', e)
    sys.exit(2)

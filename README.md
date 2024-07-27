# PoC

Install all dependencies:
```sh
pip install -r requirements.txt
```

Create a `.env` file and add `OPENAPI_API_KEY` into it.

## V1

A really basic test, where the UI gathered data is used to assemble a simple request to OpenAI's servers.

```sh
streamlit run src/v1/index.py
```

## Sandbox

Some tests, just playing around to understand how things work.

### Prompt LLM Parser

A simple script using langchain to generate a structured JSON response.

### RAG

Build a vector db (ChromaDB) basing its embeddings on *.md* files. Thus, query it on that specific document(s). The response also tracks the documents containing the answer.
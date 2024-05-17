## Quick Sample Implementation of RAG based model using FastAPI, Langchain and on-disk ChromaDB

The project has a documents folder that is used to create a knowledge base for the chatbot. The embedding and foundational models used is OpenAI's 3.5-turbo model

# Steps to run:
1. Create a virtual environment for this project [Optional but recommended]
2. Add a `.env` file in the main directory and add an OpenAI API key with the parameter name `OPENAI_API_KEY`
3. Install requirements with `pip install -r requirements.txt`
4. Run FastAPI server with `uvicorn server.main:app --host 0.0.0.0 --reload`
5. Open the `index.html` file in the webapp folder

# Pre-processing steps
Make an API call with `POST` on `localhost:8000/embed` to parse all documents and create embeddings.
This can be done via the _curl_ command `curl -X POST http://localhost:8000/embed`

# Few additional things that can be done to improve the responses:
1. Better chunking and embedding
2. Retrival can be improved by using better vector databases (CromaDB used for easy of doing it in memory or on disk)
3. OCR can be improved with better extraction models
4. Improvements to prompts to make it make it more attunded to legal domain
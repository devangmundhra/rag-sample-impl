import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter

def _get_pdf_files_in_directory(relative_path):
    current_directory = os.path.dirname(os.path.abspath(__file__))    
    directory_path = os.path.join(current_directory, relative_path)
    files = os.listdir(directory_path)
    pdf_files = [os.path.join(directory_path, file) for file in files if file.endswith(".pdf")]

    return pdf_files

def embed(folder_path:str="../../documents"):
 # Load documents
        docs = []
        for file_path in _get_pdf_files_in_directory(folder_path):
            print(file_path)
            loader = PyPDFLoader(file_path)
            docs.extend(loader.load())
        
        # Split documents
        text_splitter = TokenTextSplitter(chunk_size=2000, chunk_overlap=300)

        splits = text_splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(persist_directory="../chroma_db", documents=splits, embedding=OpenAIEmbeddings())
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import os

def load_documets(path_file):
    loader = PyPDFLoader(path_file)
    pages = loader.load_and_split()
    return pages


# test = load_documets("uploads/")

def text_splitter(pages):
     # Set a really small chunk size, just to show.
    text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
    )
    chunked = text_splitter.split_documents(pages)
    return chunked

AIzaSyBrbZofGPedoqwIoy1NaLfjiE_0MrOvY9I
# def embadding_and_save()

def embadding(texts):
    model_name = "models/embedding-001"
    api_key = "" 
    
    embeddingsss = GoogleGenerativeAIEmbeddings(model=model_name, google_api_key=api_key) # creating embeddings

    db = FAISS.from_documents(texts, embeddingsss)
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    store_data = db.save_local("saving_local")
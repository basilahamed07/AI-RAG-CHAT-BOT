from flask import Flask, request, jsonify
from flask_cors import CORS
# import openai
# import PyMuPDF
from langchain.chains import RetrievalQA
# from langchain.vectorstores import FAISS
# from langchain.embeddings import OllamaEmbeddings
# from langchain.llms import OpenAI
# import faiss
import os
import google.generativeai as genai
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Setup OpenAI API Key
my_api_key = "AIzaSyBrbZofGPedoqwIoy1NaLfjiE_0MrOvY9I"
genai.configure(api_key=my_api_key)



# Global variable to hold FAISS vector store
vector_store = None

# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_file):
    doc = PyPDFLoader()
    pages = doc.load_and_split(pdf_file)
    return pages


def chunking_data(pages):
    chunkes = RecursiveCharacterTextSplitter(
         chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
    )
    chunked_data = chunkes.create_documents(pages)
    return chunked_data


# Initialize LangChain LLM and Vector Store (FAISS)
llm = OpenAI(temperature=0)

# Placeholder for FAISS vector store (in-memory)
vector_store = None


# Initialize LangChain LLM and FAISS vector store (memory)
# llm = OpenAI(temperature=0)

# Endpoint to upload PDF and process text into vector store
@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    global vector_store
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Extract text from the uploaded PDF
    text = extract_text_from_pdf(file)

    #chunkin the data
    chunked = chunking_data(text)


    # Convert the text to documents
    # documents = [{"page_content": text}]
    
    # Embed documents and store in FAISS index
    model_name = "models/embedding-001"
    api_key = "AIzaSyBrbZofGPedoqwIoy1NaLfjiE_0MrOvY9I" 

    embeddingsss = GoogleGenerativeAIEmbeddings(model=model_name, google_api_key=api_key) # creating embeddings

    db = FAISS.from_documents(chunked, embeddingsss)
    store_data = db.save_local("saving_local")

    return jsonify({"message": "PDF processed and ready for queries"}), 200

# Endpoint to ask questions
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "Missing question"}), 400

    # Check if the vector store exists
    if vector_store is None:
        return jsonify({"error": "No documents loaded. Please upload a PDF first."}), 400



    results = db.similarity_search(query , k= 1)
    for doc in results:
        print(f"Content: {doc.page_content}, Metadata: {doc.metadata}")
    # Set up retriever
    retriever = vector_store.as_retriever()

    # Chain the retrieval and answering process
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # Get the answer
    answer = qa_chain.run(question)
    
    return jsonify({"answer": answer}), 200

if __name__ == "__main__":
    app.run(debug=True)

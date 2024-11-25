from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from groq import Groq
from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

def get_result(path,user_question):
    model_name = "models/embedding-001"
    api_key = "AIzaSyBrbZofGPedoqwIoy1NaLfjiE_0MrOvY9I" 
    # db = FAISS.from_documents("../saving", embadding)
    embeddingsss = GoogleGenerativeAIEmbeddings(model=model_name, google_api_key=api_key) # creating embeddings
    new_vector_store = FAISS.load_local(
        path, embeddingsss, allow_dangerous_deserialization=True
    )
    results = new_vector_store.similarity_search(user_question , k=5)
    for doc in results:
        print(f"Content: {doc.page_content}, Metadata: {doc.metadata}")
    return results

def generate_answer(result, user_question):
    groq_api_key = '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'
    model = "llama3-groq-70b-8192-tool-use-preview"
    conversational_memory_length = 5
    memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)
    groq_chat = ChatGroq(
    groq_api_key=groq_api_key, 
    model_name=model
)

    chat_history = []
    system_prompt = f"Given the following text chunks:\n{result}\nGenerate a response to the query: {user_question}"
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=system_prompt
            ),  # This is the persistent system prompt that is always included at the start of the chat.
            MessagesPlaceholder(
                variable_name="chat_history"
            ),  # This placeholder will be replaced by the actual chat history during the conversation. It helps in maintaining context.
            HumanMessagePromptTemplate.from_template(
                "{human_input}"
            ),  # This template is where the user's current input will be injected into the prompt.
        ]
    )

    conversation = LLMChain(
        llm=groq_chat,  # The Groq LangChain chat object initialized earlier.
        prompt=prompt,  # The constructed prompt template.
        verbose=True,   # Enables verbose output, which can be useful for debugging.
        memory=memory,  # The conversational memory object that stores and manages the conversation history.
    )

    response = conversation.predict(human_input=user_question)
    chat_history.append({'human': user_question, 'AI': response})
    return response
    # print("Chatbot:", response)
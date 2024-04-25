import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load the embedding model
embedding_model = GoogleGenerativeAIEmbeddings(google_api_key="AIzaSyC2Bztff9XtDCDrCJfMJ8py9JaT8VkwSlY", model="models/embedding-001")
st.snow()

# Setting a Connection with the ChromaDB
db_connection = Chroma(persist_directory="./chroma_db_", embedding_function=embedding_model)

# Define retrieval function to format retrieved documents
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs) 

# Converting CHROMA db_connection to Retriever Object
retriever = db_connection.as_retriever(search_kwargs={"k": 5})

# Define chat prompt template
chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="""You are a Helpful AI Bot. 
    Your task is to provide assistance based on the context given by the user. 
    Make sure your answers are relevant and helpful."""),
    HumanMessagePromptTemplate.from_template("Answer the question based on the given context.\nContext:\n{context}\nQuestion:\n{question}\nAnswer:")
])

# Initialize chat model
chat_model = ChatGoogleGenerativeAI(google_api_key="AIzaSyC2Bztff9XtDCDrCJfMJ8py9JaT8VkwSlY", 
                                    model="gemini-1.5-pro-latest")

# Initialize output parser
output_parser = StrOutputParser()

# Define RAG chain
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | chat_template
    | chat_model
    | output_parser
)

# Streamlit UI
st.title("✨ :rainbow[RAG System] ✨")
st.subheader(":red[Develop an advanced contextual question-answering AI system, guided by the principles of the 'Leave No Context Behind' paper.]")

question = st.text_input(":blue[🤔 Please write your question:🤔]")

if st.button(":green[📝Generate Answer📣]"):
    if question:
        response = rag_chain.invoke(question)
        st.markdown("<span style='color: skyblue'>📝📣 Answer:</span> <span style='color: purple'>✨</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color: green'>{response}</span>", unsafe_allow_html=True)
    else:
        st.warning("📑💡Please retry again.")
    st.balloons() 
    
    st.markdown("<span style='color: yellow'>Thank you for exploring the RAG System! Feel free to ask any questions or provide feedback.</span>", unsafe_allow_html=True)

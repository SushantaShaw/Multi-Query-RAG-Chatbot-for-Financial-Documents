from llm_generation import generation
import yaml
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_cohere import ChatCohere
from langchain_huggingface import HuggingFaceEmbeddings
from fastapi import FastAPI
from langchain_core.messages import HumanMessage,AIMessage
from langchain_groq import ChatGroq

#loading keys
load_dotenv()

cohere_api_key = os.getenv('COHERE_API_KEY')

#loading config files
config_path='./config.yaml'
with open(config_path) as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.getenv('langsmith_api_key') #type:ignore
os.environ['LANGCHAIN_PROJECT'] = config['langsmith_project']

llm = ChatCohere(cohere_api_key=cohere_api_key,model='command-r') #type:ignore

#intializig the embedding model
# embeddings = CohereEmbeddings()
embeddings = HuggingFaceEmbeddings(model_name='multi-qa-MiniLM-L6-cos-v1')

#load the vector database from the local storage
db = Chroma(embedding_function=embeddings,persist_directory=config["db_directory"])
retriever = db.as_retriever()

app = FastAPI()
chat_history = []

@app.get("/generate/")
def generate_language(user_input: str):
    generation_model = generation(llm=llm,retriever=retriever)
    print(len(chat_history))
    
    response = generation_model.generate(user_input,chat_history)

    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response))
    # if len(chat_history)+1%10==0:
    #     summarized_text = generation_model.summarize(chat_history)['content']
    #     chat_history = []
    #     chat_history.append(HumanMessage(content=summarized_text))
    return {'output':response}
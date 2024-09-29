from llm_generation import generation
import yaml
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_cohere.llms import Cohere
from langchain_cohere import CohereEmbeddings,ChatCohere
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage,AIMessage
import warnings

warnings.filterwarnings('ignore')

load_dotenv()
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



if __name__=='__main__':
    cohere_api_key = os.getenv('COHERE_API_KEY')
    llm = ChatCohere(cohere_api_key=cohere_api_key,model='command-r') #type:ignore

    #intializig the embedding model
    # embeddings = CohereEmbeddings()
    embeddings = HuggingFaceEmbeddings(model_name='multi-qa-MiniLM-L6-cos-v1')

    #load the vector database from the local storage
    db = Chroma(embedding_function=embeddings,persist_directory=config["db_directory"])
    retriever = db.as_retriever()

    generation_model = generation(llm=llm,retriever=retriever)
    chat_history = [HumanMessage(content="I am Sushanta"),AIMessage(content='Hello Sushanta'),HumanMessage(content="I am a college student and looking for a good college")]
    response = generation_model.summarize(chat_history)
    print(response)

    # while True:
    #     user_input = input("You: ")
    #     if user_input.lower()=="exit":
    #         break

    #     response = generation_model.generate(user_input,chat_history)
    #     print("Chatbot: ",response)
    #     chat_history.append(HumanMessage(content=user_input))
    #     chat_history.append(AIMessage(content=response))

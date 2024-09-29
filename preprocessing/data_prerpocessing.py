import warnings
warnings.filterwarnings("ignore")
import yaml
import os
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()


config_path='.\config.yaml'
with open(config_path) as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print(config)

#loading data
pdf_loader = PyPDFDirectoryLoader(config['input_files_path'])
docs = pdf_loader.load()

#intializig the embedding model
# embeddings = CohereEmbeddings()
embeddings = HuggingFaceEmbeddings(model_name='multi-qa-MiniLM-L6-cos-v1')

#splitting text into chunks
splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=400,chunk_overlap=50)
texts = splitter.split_documents(docs)

#creating and loading the embeddings
chroma_db = Chroma.from_documents(texts,collection_name=config["db_collection_name"],embedding=embeddings,persist_directory=config["db_directory"])
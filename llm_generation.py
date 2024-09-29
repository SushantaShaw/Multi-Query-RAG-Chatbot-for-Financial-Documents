from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder,PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import StrOutputParser
from langchain.load import dumps, loads
from transformers import AutoModelForSequenceClassification
from logger import setup_logger


class generation:
    def __init__(self,llm,retriever):
        self.llm = llm
        self.retriever = retriever
        self.logger = setup_logger()
        self.model = AutoModelForSequenceClassification.from_pretrained('vectara/hallucination_evaluation_model', trust_remote_code=True)

    def get_cleaned_output(self,text:list):
        question = list(filter(None, text))
        question = [i for i in question if i[0].isnumeric()]
        return question

    def get_unique_union(self,documents: list[list]):
        """ Unique union of retrieved docs """
        # Flatten list of lists, and convert each Document to string
        flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
        # Get unique documents
        unique_docs = list(set(flattened_docs))
        # Return
        return [loads(doc) for doc in unique_docs]

    def generate(self,question,chat_history):

        #Below code is for query transformation
        template = """You are an AI language model assistant. Your task is to generate 4 
        different versions of the given user question to retrieve relevant documents from a vector 
        database. By generating multiple perspectives on the user question, your goal is to help
        the user overcome some of the limitations of the distance-based similarity search. 
        Provide these alternative questions separated by newlines and each new quetion should start with numerical order. Original question: {question}"""
        prompt_perspectives = ChatPromptTemplate.from_template(template)


        generate_queries = (
            prompt_perspectives 
            | self.llm
            | StrOutputParser() 
            | (lambda x:x.split('\n'))
        )

        retrieval_chain = generate_queries | self.get_cleaned_output |self.retriever.map() | self.get_unique_union

        ##Below code is for augmented query generation
        # RAG
        template = """You are a converstaional chtabot which retrieve data from documents. Answer the question based only on the following context in short and crisp manner. 
        Please answer in list wherever it is applicable . Dont use your own data and always use the vectordb context that is provided. 
        Incase the answer is not present in the context please answer "This is not in my context. I have knowledge of ICICI credit cards only." And dont take third part sorces to answer.
        When user asks you to send the data in a list. Just provide the names in a list. Nothing else:\n
        context:{context}
        """
        prompt = ChatPromptTemplate.from_messages([
            ('system',template),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{question}")
        ])

        chain = (
            {"context": retrieval_chain,'chat_history':lambda x : chat_history, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        out = chain.invoke(question)
        self.logger.info(f"input:{input}")
        self.logger.info(f"output:{out}")
        return out
    
    def summarize(self,chat_history):
        template = '''You are a very good assistant who does really good work summarizing long text based on the chat history that is provided.
        chat_history:{history}
        '''
        prompt = PromptTemplate.from_template(template=template)

        chain = prompt|self.llm
        summarized_text = chain.invoke({'history':chat_history})
        return summarized_text
    
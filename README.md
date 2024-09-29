# This is a guide on how to run the app in your local

1. create a python virtual env.
2. run pip install -r requirements.txt
3. Clone the project into your local
4. Create a cohere and langsmith api key
5. Create .env file and store the two keys as following
    COHERE_API_KEY=''
    langsmith_api_key=''
6. Then open two terminals
7. In one terminal run 
    ```bash
    fastapi dev fastapi_rag.py
8. Once that is up, open another terminal and run
    ```bash
    streamlit run streamlit_app.py
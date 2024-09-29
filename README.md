# This is a guide on how to run the app in your local

1. create a python virtual env.
2. run
   ```bash
   pip install -r requirements.txt
4. Clone the project into your local
5. Create a cohere and langsmith api key
6. Create .env file and store the two keys as following
   COHERE_API_KEY=''
   langsmith_api_key=''
8. Then open two terminals
9. In one terminal run 
    ```bash
    fastapi dev fastapi_rag.py
10. Once that is up, open another terminal and run
    ```bash
    streamlit run streamlit_app.py

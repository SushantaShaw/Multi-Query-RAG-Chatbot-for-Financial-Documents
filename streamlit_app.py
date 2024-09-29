import streamlit as st # type: ignore
import requests
from langchain_core.messages import HumanMessage,AIMessage

import requests

# query = "Tell me the credit card names"
# response = requests.get("http://127.0.0.1:8000/generate/",params={'input':query})
# print(response.json())

# Check if the request was successful



def generate_response(user_input):
    url = "http://127.0.0.1:8000/generate/"
    response = requests.get(url,params={'user_input':user_input})
    answer = response.json()
    if response.status_code == 200:
    # Parse the JSON response
        answer = response.json()
        return answer['output']
    else:
        return ("Error:", response.status_code, response.text)

# Streamlit app
def main():
    st.title("Credit card Chatbot")
    st.write("This is a chatbot fueled by credit card info documents.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Generate AI response
        with st.spinner("Generating response..."):
            ai_response = generate_response(user_input)

        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

if __name__ == "__main__":
    main()
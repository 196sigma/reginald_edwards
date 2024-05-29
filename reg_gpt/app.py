# app.py
import time
import json
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load your OpenAI API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

current_date = time.strftime("%Y-%m-%d %H:%M:%S")
# data store for prompts and responses
# jsonlines file in `chat_history.jsonl`
chat_history_file = "chat_history.jsonl"


# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

st.title("ChatGPT Streamlit App")

# Dropdown to select the model type
model_options = ["gpt-3.5-turbo", "gpt-4o", "gpt--4-turbo"]
selected_model = st.selectbox("Select model", model_options)
# Enter passphrase to access the app
attempts = 0
password = st.text_input("Enter password:", type="password")
if (password != "studyhall1026") and (attempts < 3):
    st.write("Incorrect password. Please try again.")
    attempts += 1
    st.stop()
if attempts == 3:
    st.write("Too many attempts. Please try again later.")
    st.stop()
# Text input for user query
user_input = st.text_input("Enter your message:", "")

# Function to call OpenAI API using the selected model
def get_chatgpt_response(prompt, model):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            model=model
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return str(e)

# Display response
if user_input:
    response = get_chatgpt_response(user_input, selected_model)
    st.write("ChatGPT response:")
    st.write(response)

current_chat = {"date": current_date, "prompt": user_input, "response": response, "model":selected_model}
with open(chat_history_file, "a") as file:
    file.write(json.dumps(current_chat) + "\n")
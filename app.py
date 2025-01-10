import google.generativeai as genai
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st
import json


class Chatbot():
    def __init__(self, encoder, model):
        self.__api_key = os.getenv("API_KEY")
        self.encoder = encoder
        self.model = model

    def separate(self, indexed_content):
        titles = {key: value['title'] for key, value in indexed_content.items()}
        content = {key: value['content'] for key, value in indexed_content.items()}
        return titles, content
    
    def chat_bot(self, indexed_content, query):
        titles, content = self.separate(indexed_content)

        titles_embedding = list(titles.values())
        titles_embedding = self.encoder.encode(titles_embedding)
        query_embedding = self.encoder.encode([query])
        similarities = cosine_similarity(query_embedding, titles_embedding)
        most_similar_index = np.argmax(similarities)
        tostring = str(most_similar_index)
        genai.configure(api_key=self.__api_key)

        response = self.model.generate_content(f"Answer this query{query}, base on the information {content[tostring]}")
        return response
def prepare_chatbot():
        encoder = SentenceTransformer('all-MiniLM-L6-v2')
        model = genai.GenerativeModel("gemini-1.5-flash")
        return Chatbot(encoder=encoder, model=model)


def main():
    st.title("Presight's Privacy Policy Chatbot")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if 'indexed_content' not in st.session_state:
        with open("data.json", "r", encoding="utf-8") as file:
            st.session_state.indexed_content = json.load(file)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("Type your question:"):
        st.session_state.messages.append(
            {
                "role": "user",
                "content":prompt
            }
        )
        with st.chat_message('user'):
            st.markdown(prompt)
    #Tạo phản hồi cho mô hình
        chatbot = prepare_chatbot()
        response = chatbot.chat_bot(st.session_state.indexed_content, prompt)
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content":response.text
            }
        )
        with st.chat_message('assistant'):
            st.markdown(response.text)
        
if __name__ == "__main__":
    main()
import google.generativeai as genai
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By 
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import streamlit as st


def scrapingData(url):
    DRIVER_PATH = "C:/path/to/chromedriver/chromedriver-win64/chromedriver.exe"
    options = Options()
    options.add_argument('--headless')
    service = Service(executable_path=DRIVER_PATH)  
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    
    elements = driver.find_elements(By.XPATH, "//h2 | //p | //ul | //i")
    content = []
    headers = []

    for element in elements:
        text = element.text.strip() 
        if element.tag_name == 'h2' or element.tag_name == 'i':
            headers.append(text)
        if not text: 
            continue
        if element.tag_name == 'ul':
            li_elements = element.find_elements(By.TAG_NAME, 'li')
            list_items = [li.text.strip() for li in li_elements if li.text.strip()]
            if list_items:
                content.append(" ".join(list_items))  
        else:
            content.append(text)

    driver.quit()
    return content,headers

url = 'https://www.presight.io/privacy-policy.html'
content, headers = scrapingData(url)


def index_content(content, headers):
    indexed_content = {}
    current_index = None
    title = None
    content_list = []
    for item in content:
        # Kiểm tra nếu item có trong headers
        if item in headers:
            # Nếu có title mới, lưu lại title và content cũ
            if current_index is not None:
                indexed_content[current_index] = {
                    'title': title,
                    'content': content_list
                }   
            # Thiết lập title mới và làm mới content
            title = item
            content_list = []
            current_index = len(indexed_content)  
        else:
            # Nếu không trùng, thêm item vào content của title hiện tại
            content_list.append(item)
    
    # Lưu phần cuối cùng
    if current_index is not None:
        indexed_content[current_index] = {
            'title': title,
            'content': content_list
        }
    return indexed_content

indexed_content = index_content(content, headers)
indexed_content[0] = {'title': 'PRIVACY POLICY - Last update', 'content': ['Last updated 15 Sep 2023']}
indexed_content[1]['title'] = 'PRIVACY POLICY - Description'
indexed_content[3]['content'] = 'Personal Data, Usage Data'
indexed_content[8]['content'] = 'Accessing Your Personal Information, Automated Edit Checks'

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

        genai.configure(api_key=self.__api_key)

        response = self.model.generate_content(f"Answer this query{query}, base on the information {content[most_similar_index]}")
        return response




st.title("Chatbot about Privacy Policy of Presight")
st.image("tải xuống (1).jpg", width=200)

query = st.text_input("Ask your query:")
@st.cache_resource
def prepare_chatbot():
    encoder = SentenceTransformer('all-MiniLM-L6-v2')
    model = genai.GenerativeModel("gemini-1.5-flash")
    return Chatbot(encoder=encoder, model=model)
st.write("Preparing chatbot...")
chatbot = prepare_chatbot()
if query:
    st.write("Getting response...")
    try:
        response = chatbot.chat_bot(indexed_content, query)
        st.write("### Response")
        st.write(response.text)
    except Exception as e:
        st.write("An error occurred while processing your query.")
        st.error(str(e))
else:
    st.write("Please enter a query to get started.")

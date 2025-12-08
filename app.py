import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Funding App")
st.title("It Works!")

api_key = st.text_input("API Key")
if api_key:
    genai.configure(api_key=api_key)
    st.success("API Configured!")
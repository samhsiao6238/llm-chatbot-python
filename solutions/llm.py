import streamlit as st
from langchain_openai import ChatOpenAI
# import os

# 建立 ChatOpenAI 實體
llm = ChatOpenAI(
    openai_api_key=st.secrets["OPENAI_API_KEY"],
    model=st.secrets["OPENAI_MODEL"],
    # openai_api_key=os.getenv("OPENAI_API_KEY"),
    # model=os.getenv("OPENAI_MODEL"),
)
from langchain_openai import OpenAIEmbeddings

# OpenAIEmbeddings 是用來生成和處理嵌入向量（embeddings）
# 這些嵌入向量是從使用 OpenAI 模型（如 GPT-4）生成的文本中獲取的
embeddings = OpenAIEmbeddings(
    openai_api_key=st.secrets["OPENAI_API_KEY"]
    # openai_api_key=os.getenv("OPENAI_API_KEY")
)

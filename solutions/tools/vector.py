import streamlit as st
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
# from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains import RetrievalQA
from solutions.llm import llm, embeddings
# import os

# 使用 Neo4jVector.from_existing_index 方法創建一個 Neo4jVector
neo4jvector = Neo4jVector.from_existing_index(
    # 用於嵌入用戶輸入的嵌入對象
    embeddings,
    # Neo4j 實例的 URI、帳號密碼
    url=st.secrets["NEO4J_URI"],
    username=st.secrets["NEO4J_USERNAME"],
    password=st.secrets["NEO4J_PASSWORD"],
    # url=os.getenv("NEO4J_URI"),
    # username=os.getenv("NEO4J_USERNAME"),
    # password=os.getenv("NEO4J_PASSWORD"),        
    # 索引名稱
    index_name="moviePlots",
    # 用於填充索引的節點標籤
    node_label="Movie",
    # 保存原始純文本值的屬性名稱
    text_node_property="plot",
    # 保存原始文本嵌入的屬性名稱
    embedding_node_property="plotEmbedding",
    #
    retrieval_query="""
        RETURN
            node.plot AS text,
            score,
            {
                title: node.title,
                directors: [ (person)-[:DIRECTED]->(node) | person.name ],
                actors: [ (person)-[r:ACTED_IN]->(node) | [person.name, r.role] ],
                tmdbId: node.tmdbId,
                source: 'https://www.themoviedb.org/movie/'+ node.tmdbId
            } AS metadata
    """,
)
# 創建 Neo4jVector 的 Retriever
retriever = neo4jvector.as_retriever()
# 創建新的 RetrievalQA Chain
kg_qa = RetrievalQA.from_chain_type(
    # 處理鏈的 LLM
    llm,
    # 直接將文檔插入提示並將提示傳遞給 LLM
    chain_type="stuff",
    # 使用之前創建的 Neo4jVectorRetriever
    retriever=retriever,
)

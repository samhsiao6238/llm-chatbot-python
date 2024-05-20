from langchain.chains import GraphCypherQAChain
from langchain.prompts.prompt import PromptTemplate
from solutions.llm import llm
from solutions.graph import graph

# 添加定義 `模式 Schema`
# SCHEMA = """
# (Movie)-[:DIRECTED_BY]->(Director)
# """

# 更新模板以包含模式 Schema
CYPHER_GENERATION_TEMPLATE = """
你是一名專業的 Neo4j 開發者，將用戶的問題轉換為 Cypher 語句，以回答有關電影的問題並提供推薦。
根據模式轉換用戶的問題。

只使用模式中提供的關係類型和屬性。
不使用任何未提供的關係類型或屬性。

Fine Tuning:

對於以 "The" 開頭的電影標題，將 "The" 移到末尾。例如 "The 39 Steps" 變為 "39 Steps, The" 或 "the matrix" 變為 "Matrix, The"。


Schema:
{schema}

Question:
{question}

Cypher Query:
"""

# 使用模板創建一個 PromptTemplate 對象
cypher_prompt = PromptTemplate.from_template(CYPHER_GENERATION_TEMPLATE)

# 創建一個 GraphCypherQAChain 對象，用於執行基於圖數據庫的問答
# 這個函數會在 `agent.py` 中的 `Tool.from_function` 被調用
cypher_qa = GraphCypherQAChain.from_llm(
    # 使用的語言模型
    llm,
    # 使用的圖數據庫
    # 官方說明中並未提及這個參數，但因為 `langchain_community.chains.graph_qa.cypher.py`
    # 需要傳遞這個參數
    graph=graph,
    # 啟用詳細日誌，設置為 `True` 的時候會顯示詳細的 Embedding
    verbose=False,
    # 使用的 Cypher 查詢模板
    cypher_prompt=cypher_prompt
)

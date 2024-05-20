from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from solutions.llm import llm
# 在 agent.py 中註冊 Retrieval Chain 作為工具，先導入 kg_qa
from solutions.tools.vector import kg_qa
from solutions.tools.finetuned import cypher_qa
# 導入 logging
import logging

# 設置日誌記錄
logging.basicConfig(level=logging.DEBUG)

# 在工具陣列中添加 kg_qa
tools = [
    # 處理一般聊天對話，涵蓋所有其他工具未涵蓋的問題和請求。
    Tool.from_function(
        name="General Chat",
        description="處理一般聊天對話，涵蓋所有其他工具未涵蓋的問題和請求。",
        func=llm.invoke,
        # 不要直接輸出
        return_direct=False,
    ),
    # 用於基於向量搜索的電影情節信息檢索。
    # 如果問題涉及查找與特定電影情節相似的電影，並且需要使用向量搜索技術，會使用此工具。
    Tool.from_function(
        name="Vector Search Index",
        description="用於基於向量搜索的電影情節信息檢索。",
        func=kg_qa,
        # 不要直接輸出
        return_direct=False,
    ),
    # 用於使用 Cypher 查詢語句來回答有關電影的具體問題。
    # 如果問題需要從 Neo4j 數據庫中檢索電影信息，並涉及生成和執行 Cypher 查詢。
    # 注意這裡會調用 cypher_qa
    Tool.from_function(
        # 這名稱會在終端機中顯示為 `Action：Cypher QA`
        name="Cypher QA",
        description="用於使用 Cypher 查詢語句來回答有關電影的具體問題。",
        # 調用 finetuned.py 中自訂的函數 cypher_qa
        func=cypher_qa,
        # 不可以直接回應，否則會出現解析錯誤
        return_direct=False,
    ),
]

# 調用 langchain 函數 ConversationBufferWindowMemory
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=5,
    return_messages=True,
)

# 調用 langchain 函數 hub.pull() 生成
agent_prompt = hub.pull("hwchase17/react-chat")
# 調用 langchain 函數 create_react_agent
# 傳入 `llm`、`tools`、`Agent 的回應`
agent = create_react_agent(llm, tools, agent_prompt)
# 透過 AgentExecutor 類建立代理執行物件
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)


# 修正的腳本
def generate_response(prompt):
    # 日誌
    logging.debug(f'Prompt: {prompt}')
    print(f'=> generate_response 函數輸出 prompt -> {prompt}')
    try:
        print('=> generate_response 函數進入 try')
        # 回應
        response = agent_executor.invoke({"input": prompt})
        # 日誌
        logging.debug(f'Response: {response}')
        print(f'=> response -> {response}')
        # 獲取回應中的 'output' 字段，如果不存在則為 None
        output = response.get('output', None)
        if output is None:
            return "=> 回應 `response` 中沒有結果 `output`。"

        if isinstance(output, dict):
            print('=> agent.py -> 備註：回應是一個 dict=')
            # 將 dict 的項轉換為字符串並連接
            response_output = ', '.join([f"{key}: {value}" for key, value in output.items()])
        elif isinstance(output, str):
            response_output = output
        else:
            raise ValueError(f"=> 非預期的結果型態 `output type` -> {type(output)}")

        # 確保 response_output 是字符串或列表
        if not isinstance(response_output, str):
            raise ValueError(f"=> 無效的回應結果型態 `response output type` -> {type(response_output)}")

        return response_output
    except Exception as e:
        print('=> generate_response 無法解析 -> 回應發生錯誤=')
        # 日誌
        logging.error(f'Error parsing response: {e}')
        return f"=> 錯誤的 response -> {str(e)}"
    finally:
        pass

# 保留官方原始代碼作為參考
# def generate_response(prompt):
#     response = agent_executor.invoke({"input": prompt})
#     return response["output"]


# 加入測試代碼
print('== 進行測試 ==')
prompt = "資料庫中的第一個節點訊息是什麼？"
# prompt = "以色列與巴基斯坦之間的恩怨情仇起因為何？"
# 調用 generate_response
response = generate_response(prompt)
print(response)

import streamlit as st
# 從自訂模組中導入函數
from utils import write_message
# 導入生成回覆的函數
from solutions.agent import generate_response

# 設定瀏覽器頁籤及圖標
st.set_page_config("大柱子", page_icon=":movie_camera:")

# 假如訊息狀態字典 `session_state` 中沒有鍵 `messages`
if "messages" not in st.session_state:
    # 表示這是初次啟動，所以在鍵 `messages` 儲存第一筆資料
    # 稍後會在其他程序中來遍歷這個字典，用以顯示對話
    st.session_state.messages = [{
        "role": "assistant",
        "content": "哈囉，這是初次啟動，請問需要什麼服務？"
    },]


# 自訂函數：處理提交，傳入一個參數 `message`，最後會顯示在 `助手` 端
def handle_submit(message):
    # 提交時，會先顯示這個字串
    with st.spinner('讓我思考一下...'):
        # 調用自訂函數 `generate_response`
        # 同時傳入 `handle_submit` 函數所取得的傳入字串來生成回應
        response = generate_response(message)
        # 調用自訂函數 `write_message` 將 `生成的回應` 傳入
        # 並以 `助手` 身份來寫入這個生成的回應
        write_message('assistant', response)


# 遍歷訊息狀態中的鍵 `messages` 的值
for message in st.session_state.messages:
    # 調用寫入訊息的函數
    # 因為參數 `save` 是 `False`，所以不會儲存，直接執行 `顯示`
    write_message(
        message['role'],
        message['content'],
        save=False
    )

# 假如用戶輸入了訊息
if prompt := st.chat_input("怎麼了？有話就說吧～"):
    # 調用寫入函數，這時候會執行儲存然後顯示在 `user` 端
    write_message('user', prompt)
    # 提交並顯示在助手端
    handle_submit(prompt)

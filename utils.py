import streamlit as st


# 自訂一個寫入訊息的函數，參數有：角色、內容，並預設會儲存
def write_message(role, content, save=True):
    # 儲存
    if save:
        # 依據傳入的角色將訊息寫入 session_state
        st.session_state.messages.append({
            "role": role, "content": content
        })
    with st.chat_message(role):
        # 依據角色，將對話顯示在客戶端或是服務端
        st.markdown(content)

import streamlit as st
from langchain_openai import AzureChatOpenAI
from langchain.schema import (HumanMessage, AIMessage)
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    llm = AzureChatOpenAI(
    azure_endpoint= os.environ['AZUREOPENAI_API_ENDPOINT'],
    openai_api_version="2023-03-15-preview",
    deployment_name= os.environ['DEPLOYMENT_NAME_GPT'],
    openai_api_key= os.environ['AZUREOPENAI_API_KEY'],
    openai_api_type="azure",
    )

  # ページの設定
    st.set_page_config(
        page_title="My Great ChatGPT",
        page_icon="😎"
    )
    st.header("My Great ChatGPT 😎")

    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ユーザーの入力を監視
    if user_input := st.chat_input("聞きたいことを入力してね！"):
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("GPT is typing ..."):
            response = llm.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))

    # チャット履歴の表示
    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:
            st.write(f"System message: {message.content}")

if __name__ == '__main__':
    main()
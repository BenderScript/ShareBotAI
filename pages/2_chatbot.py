import streamlit as st

st.set_page_config(page_title="Kosha GenAI", page_icon=":rocket:", layout="wide")
st.title("GenAI - Sharepoint URL Dynamic Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.chatbot_created:
    text_docs = st.session_state.text_doc_processor
    if prompt := st.chat_input("What is up?"):
        system_prompt = ("You are a helpful assistant that will answer questions about research conducted by a "
                         "software engineer on the limitations of GPT-3\n\n")
        st.session_state.messages.append({"role": "system", "content": system_prompt})
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            conv_chain_full_response = text_docs.text_conv_chain({"question": prompt})
            full_response += conv_chain_full_response["answer"]
            message_placeholder.markdown(full_response + "▌")
            # message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.error("Chatbot not created yet. Ingest data first.")
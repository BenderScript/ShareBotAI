import os
from streamlit_extras.switch_page_button import switch_page
import streamlit as st
from sharepoint_documents import connect_to_sharepoint, download_files, traverse_directory

st.set_page_config(page_title="Sharepoint GenAI RAG Chatbot", page_icon=":rocket:", layout="wide")
st.title("GenAI - Sharepoint On-Demand RAG Chatbot")

if "downloaded_files" not in st.session_state:
    with st.status("Preparing Chatbot...", expanded=True, state="running") as status:
        text_doc_processor = st.session_state.text_doc_processor
        status.write(f"Connecting to Sharepoint: {st.session_state.sharepoint_url}/"
                     f"{st.session_state.sharepoint_folder}...")
        folder = connect_to_sharepoint(st.session_state)
        if folder is None:
            st.error("Could not connect to Sharepoint")
            switch_page("stop")
        status.write(f"Downloading files...")
        file_paths = download_files(folder, st.session_state.temp_dir)
        if file_paths is None:
            st.error("Could not download files")
            switch_page("stop")
        file_names = [os.path.basename(path) for path in file_paths]
        # Set state
        st.session_state.downloaded_files = file_paths
        status.write(f"Downloaded files {file_names}")
        if file_names is None:
            st.error("No files downloaded")
            switch_page("stop")
        status.write(f"Loading files for GenAI processing...")
        loaded_docs = traverse_directory(st.session_state.temp_dir)
        # Add loaded docs to docs class
        text_doc_processor.text_docs = loaded_docs
        if loaded_docs is None:
            st.error("No files loaded")
            switch_page("stop")
        texts = text_doc_processor.split_text_docs()
        if not texts:
            status.write(f"Error splitting texts...")
            switch_page("stop")
        status.write(f"Inserting texts into VectorDB...")
        if text_doc_processor.create_text_retriever():
            status.write(f"Creating Chatbot...")
            if text_doc_processor.create_text_conv_chain():
                status.update(label="Chatbot created!", state="complete", expanded=True)
                st.session_state.chatbot_created = True
                switch_page("chatbot")
            else:
                status.write(f"Error creating chatbot...")
                switch_page("stop")

        else:
            status.write(f"Error creating text retriever...")
            switch_page("stop")






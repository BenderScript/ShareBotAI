import os
import tempfile
import glob
import shutil

import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.switch_page_button import switch_page
from text_docs_processor import TextDocProcessor


def remove_temp_folders(temp_folder_path="."):
    """
    Removes temporary folders with a specific naming pattern from the given path.

    :param temp_folder_path: The path where the temporary folders are located.
    """
    # Use glob to find all folders that match the naming pattern
    temp_folders = glob.glob(os.path.join(temp_folder_path, 'tmp*'))

    # Loop through the folders and remove them
    for folder in temp_folders:
        try:
            # Use shutil.rmtree to remove folders that might contain files
            shutil.rmtree(folder)
            print(f"Removed folder: {folder}")
        except OSError as e:
            print(f"Error removing folder {folder}: {e}")


st.set_page_config(page_title="Sharepoint GenAI RAG Chatbot", page_icon=":rocket:", layout="wide")
st.title("GenAI - Sharepoint URL Dynamic Chatbot")

load_dotenv(override=True, dotenv_path=".env")  # take environment variables from .env.

# Streamlit integration
if 'has_run' not in st.session_state:
    remove_temp_folders()  # Adjust path if necessary
    st.session_state['has_run'] = True

col1, col2 = st.columns(2)

with col1:
    sharepoint_url = st.text_input('Sharepoint URL', os.getenv("SHAREPOINT_SITE_URL"))
    st.write('The Sharepoint URL is', sharepoint_url)

    sharepoint_folder = st.text_input('Sharepoint folder', os.getenv("SHAREPOINT_FOLDER"))
    st.write('The Sharepoint folder is', sharepoint_folder)

# Initialization
if 'sharepoint_url' not in st.session_state:
    st.session_state.sharepoint_url = sharepoint_url

if 'sharepoint_folder' not in st.session_state:
    st.session_state.sharepoint_folder = sharepoint_folder

if "temp_dir" not in st.session_state:
    st.session_state.temp_dir = tempfile.mkdtemp(dir=".")

# Initialize TextDocProcessor
if 'text_doc_processor' not in st.session_state:
    st.session_state.text_doc_processor = TextDocProcessor(temp_dir=st.session_state.temp_dir)

if st.button('Next'):
    switch_page("documents")

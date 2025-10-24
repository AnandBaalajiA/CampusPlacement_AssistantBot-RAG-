"""
Text chunking utilities
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from flask import current_app

def create_text_splitter():
    """Create configured text splitter"""
    return RecursiveCharacterTextSplitter(
        chunk_size=current_app.config['CHUNK_SIZE'],
        chunk_overlap=current_app.config['CHUNK_OVERLAP'],
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

def chunk_text(text):
    """Split text into chunks"""
    splitter = create_text_splitter()
    return splitter.split_text(text)

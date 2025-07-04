import streamlit as st

def upload_pdf():
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    if uploaded_file is not None:
        return uploaded_file
    return None

def validate_pdf(uploaded_file):
    if uploaded_file.type != "application/pdf":
        st.error("Please upload a valid PDF file.")
        return False
    return True
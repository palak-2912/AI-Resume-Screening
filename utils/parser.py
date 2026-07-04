import pdfplumber
from docx import Document
import os

def extract_text(filepath):
    text = ""

    # Check file extension
    extension = os.path.splitext(filepath)[1].lower()

    if extension == ".pdf":
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    elif extension == ".docx":
        doc = Document(filepath)

        for para in doc.paragraphs:
            text += para.text + "\n"

    return text
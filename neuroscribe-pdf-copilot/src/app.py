from dotenv import load_dotenv
import openai, os, streamlit as st
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
import speech_recognition as sr

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Voice recognition helper
def listen_for_command():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("🎤 Listening...")
            audio = r.listen(source, timeout=5)
        command = r.recognize_google(audio)
        st.success(f"Recognized: {command}")
        return command.lower()
    except Exception as e:
        st.error(f"Voice error: {str(e)}")
        return None

# Existing GPT and PDF functions remain the same
def rewrite_with_gpt(prompt, text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a PDF editor copilot."},
            {"role": "user", "content": f"{prompt}: {text}"}
        ]
    )
    return response.choices[0].message.content

def extract_text(pdf_stream):
    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    blocks = []
    for i in range(len(doc)):
        for span in doc[i].get_text("dict")["blocks"]:
            for line in span.get("lines", []):
                for s in line.get("spans", []):
                    blocks.append({
                        "page": i,
                        "text": s["text"],
                        "bbox": s["bbox"],
                        "font": s["font"],
                        "size": s["size"]
                    })
    return blocks

def rebuild_pdf(pdf_stream, edits):
    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    for item in edits:
        pg = doc.load_page(item["page"])
        x0, y0, x1, y1 = item["bbox"]
        pg.add_redact_annot((x0, y0, x1, y1), fill=(255,255,255))
        pg.apply_redactions()
        pg.insert_text((x0, y0), item["edited_text"], fontname=item["font"], fontsize=item["size"])
    return doc

# Enhanced UI with voice commands
st.set_page_config(page_title="NeuroScribe Copilot", layout="wide")
st.title("🧠 NeuroScribe PDF Copilot")

uploaded_pdf = st.file_uploader("📄 Upload your PDF", type="pdf")

if uploaded_pdf:
    pdf_bytes = uploaded_pdf.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text_data = extract_text(pdf_bytes)
    edited_data = []

    for pg_num in range(len(doc)):
        st.subheader(f"Page {pg_num+1}")
        img = Image.frombytes("RGB", *doc[pg_num].get_pixmap().size, doc[pg_num].get_pixmap().samples)
        st.image(img, use_column_width=True)

        for item in [x for x in text_data if x["page"] == pg_num]:
            col1, col2, col3 = st.columns([3,1,1])
            with col1:
                new_text = st.text_area("Edit Text", value=item["text"], key=str(item["bbox"]))
                if st.button("🎤 Speak Text", key=f"speak_{item['bbox']}"):
                    if text := listen_for_command():
                        st.session_state[str(item["bbox"])] = text
                        st.experimental_rerun()
            with col2:
                cmd = st.selectbox("Copilot Command", 
                    ["Keep", "Formal", "Friendly", "Summarize", "Erase"], 
                    key="cmd"+str(item["bbox"]))
            with col3:
                if st.button("🎤 Voice Command", key=f"voice_{item['bbox']}"):
                    if command := listen_for_command():
                        cmd_map = {
                            "formal": "Formal",
                            "friendly": "Friendly",
                            "summarize": "Summarize",
                            "erase": "Erase"
                        }
                        matched = next((v for k,v in cmd_map.items() if k in command), None)
                        if matched:
                            st.session_state[f"cmd{str(item['bbox'])}"] = matched
                            st.experimental_rerun()

    if st.button("💾 Save & Download"):
        new_doc = rebuild_pdf(pdf_bytes, edited_data)
        buffer = BytesIO()
        new_doc.save(buffer)
        st.download_button("📥 Download PDF", buffer.getvalue(), file_name="edited_output.pdf")
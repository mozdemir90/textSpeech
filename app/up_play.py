from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os
import speech_recognition as sr

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

STATIC_FOLDER = 'static'
app.config['STATIC_FOLDER'] = STATIC_FOLDER

def text_to_speech(text, output_title="output", lang='tr'):
    output_file = f"{output_title}.mp3"
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(os.path.join(app.config['STATIC_FOLDER'], output_file))
    return output_file

def extract_text_from_pdf(pdf_path):
    # PDF işleme kütüphanesini seçin (pdfplumber, PyPDF2, vs.)
    # Bu örnekte PyPDF2 kullanılıyor.
    import PyPDF2
    
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            text += page.extractText()
    return text

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

@app.route("/")
def index():
    return render_template("index2.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        if file_path.lower().endswith(".pdf"):
            text_content = extract_text_from_pdf(file_path)
        elif file_path.lower().endswith(".txt"):
            text_content = read_text_file(file_path)
        else:
            return "Desteklenmeyen dosya formatı. Lütfen .pdf veya .txt dosyası seçin."
        
        # Generate a unique title based on the original file name
        output_title = os.path.splitext(file.filename)[0]
        output_audio_file = text_to_speech(text_content, output_title)
        return output_audio_file  # Sadece ses dosyasının adını döndürüyoruz

    return "Dosya yüklenemedi."

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True,use_reloader=False, port=5001)

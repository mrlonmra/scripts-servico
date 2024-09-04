import threading
from flask import Flask, request, jsonify
import whisper
import os
from PIL import Image
import google.generativeai as genai

# Initialize Flask and Whisper model
app = Flask(__name__)
whisper_model = whisper.load_model("base")

# Configure Gemini Generative Model
api_key = os.getenv("GEMINI_API_KEY", "AIzaSyDwLFG0VFCy34pyMnW_041gtTfu2jCNXL0")
genai.configure(api_key=api_key)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Route to handle audio file uploads and transcription
@app.route('/upload', methods=['POST'])
def upload_and_process_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filename = file.filename
    save_dir = "/content"
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, filename)
    file.save(file_path)

    result = whisper_model.transcribe(file_path)
    return jsonify({"transcription": result["text"]})

# Route to handle image file uploads and analysis
@app.route('/upload_image', methods=['POST'])
def upload_and_process_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    filename = file.filename
    save_dir = "/content"
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, filename)
    file.save(file_path)

    try:
        img = Image.open(file_path)
        response = gemini_model.generate_content(img)
        return jsonify({"analysis": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to handle text processing
@app.route('/process_text', methods=['POST'])
def process_text():
    data = request.json
    if 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data['text']

    try:
        response = gemini_model.generate_content(text)
        return jsonify({"processed_text": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def run_flask():
    app.run(host='0.0.0.0', port=6061)

# Start the Flask server in a separate thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()
flask_thread.join()

print("Servidor Flask rodando.")
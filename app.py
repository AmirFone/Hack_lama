from flask import Flask, request, redirect, url_for, render_template, jsonify
import os
import subprocess
import sys
import PyPDF2
import boto3
import random
import tempfile

sys.path.append('/Users/amirhossain/Desktop/Hack_lama')
s3_client = boto3.client('s3')
from get_statistics import get_statistics

global Script_TEXT
Script_TEXT = ""

app = Flask(__name__)


@app.route("/generate_script", methods=["GET"])
def generate_script():
    # Here you would generate your script text or get it from where it's stored
    script_text = "The script text that you want to paste in the text area."
    return script_text

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/script")
def script():
    return render_template("index.html")

@app.route("/video", methods=["POST"])
def upload_video():
    global Script_TEXT
    if "video" not in request.files:
        return jsonify({"error": "No video part"}), 400

    video_file = request.files["video"]
    if video_file.filename == "":
        return jsonify({"error": "No selected video"}), 400

    if video_file:
        video_dir = ".video"
        os.makedirs(video_dir, exist_ok=True)
        temp_video_path = os.path.join(video_dir, "temp_video.webm")
        video_file.save(temp_video_path)
        mp4_path = os.path.join(video_dir, "converted_video.mp4")
        subprocess.run(["ffmpeg", "-y", "-i", temp_video_path, "-c:v", "libx264", "-strict", "-2", mp4_path])

        upload_success = upload_file_to_s3(temp_video_path, "hackllama")
        if upload_success:
            print("Video uploaded successfully.")
        else:
            print("Failed to upload video.")

        mp3_path = os.path.join(video_dir, "extracted_audio.mp3")
        subprocess.run(["ffmpeg", "-y", "-i", temp_video_path, "-q:a", "0", "-map", "a", mp3_path])

        os.remove(temp_video_path)
    return redirect(url_for('results'))

@app.route("/results")
def results():
    global Script_TEXT
    data = get_statistics(Script_TEXT)
    upload_python_object_to_s3(data, "hackllama", "statistics_data.json")
    return render_template("results.html", data=data)  

@app.route("/text", methods=["POST"])
def process_text_or_pdf():
    global Script_TEXT
    if "text" in request.form:
        text = request.form["text"]
        Script_TEXT = text
        return jsonify({"message": "Text received and processed successfully"}), 200

    elif "pdf" in request.files:
        pdf_file = request.files["pdf"]
        if pdf_file and pdf_file.filename.endswith(".pdf"):
            pdf_text = extract_text_from_pdf(pdf_file)
            Script_TEXT = pdf_text
    upload_python_object_to_s3({"text": Script_TEXT}, "hackllama", "script_text.json")
    return jsonify({"error": "Invalid request"}), 400

def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    try:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            pdf_text += page.extractText()
    except Exception as e:
        print("Error extracting text from PDF:", str(e))
    return pdf_text

def upload_file_to_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = str(random.randint(10000, 99999)) + os.path.basename(file_path)
    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return False
    return True
def upload_python_object_to_s3(obj, bucket_name, object_name):
    try:
        tmp_file = tempfile.mkstemp()[1]
        with open(tmp_file, 'w') as f:
            json.dump(obj, f)
        upload_success = upload_file_to_s3(tmp_file, bucket_name, object_name)
        os.remove(tmp_file)
        return upload_success
    except Exception as e:
        print(f"Error uploading Python object to S3: {e}")
        return False

if __name__ == "__main__":
    app.run(debug=True, port=5003)

from flask import Flask, request, redirect, url_for, render_template, jsonify
import os
from moviepy.editor import VideoFileClip
import subprocess
import sys
import PyPDF2
import json
import boto3
import random
import tempfile
sys.path.append('/Users/amirhossain/Desktop/Hack_lama')
s3_client = boto3.client('s3')
from get_statistics import get_statistics
global Script_TEXT  # Declare the variable as global
Script_TEXT = ""    # Initialize the variable

app = Flask(__name__)
users = {"user": "password", "username": "password"}


@app.route("/")
def home():
    return render_template("login.html")  # Render the sign-in page



@app.route("/script")
def script():
    return render_template("index.html")  # Render the sign-in page




@app.route("/video", methods=["POST"])
def upload_video():
    global Script_TEXT
    global clip_counter
    if "video" not in request.files:
        return jsonify({"error": "No video part"}), 400

    video_file = request.files["video"]

    if video_file.filename == "":
        return jsonify({"error": "No selected video"}), 400

    if video_file:  # If a video is actually present
        video_dir = ".video"
        os.makedirs(video_dir, exist_ok=True)

        # Save the video to a temporary path
        temp_video_path = os.path.join(video_dir, "temp_video.webm")
        
        video_file.save(temp_video_path)

        # Convert the video to MP4
        mp4_path = os.path.join(video_dir, "converted_video.mp4")
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                temp_video_path,
                "-c:v",
                "libx264",
                "-strict",
                "-2",
                mp4_path,
            ]
        )
        upload_success = upload_file_to_s3(temp_video_path, "hackllama")
        if upload_success:
            print("Video uploaded successfully.")
        else:
            print("Failed to upload video.")

        # Extract audio as MP3
        mp3_path = os.path.join(video_dir, "extracted_audio.mp3")
        subprocess.run(
            ["ffmpeg", "-y", "-i", temp_video_path, "-q:a", "0", "-map", "a", mp3_path]
        )

        # transcribed_data = transcribe_audio(mp3_path)
        # transcribed_word_timings = extract_word_timings(transcribed_data)
        # transcribed_word_clarity = extract_word_probabilities(
        #     transcribed_data, probabilities_only=False
        # )
        # print(transcribed_word_clarity)

        # Optionally, remove the temporary webm file
        os.remove(temp_video_path)
        # Return success message
        # return render_template('results.html', data=get_statistics("hey")
    return redirect(url_for('results'))

@app.route("/results")
def results():
    global Script_TEXT
    data= get_statistics(Script_TEXT)
    print(f'weirweu_kvnk{data}')
    return render_template("results.html", data=data)  
    return jsonify({"error": "Invalid request"}), 400



@app.route("/text", methods=["POST"])
def process_text_or_pdf():
    global Script_TEXT
    if "text" in request.form:
        # If 'text' is in the form data, it's text
        text = request.form["text"]

        # Handle text processing logic here
        # print("Received text:", text)
        Script_TEXT = text

        # Return a success message
        return jsonify({"message": "Text received and processed successfully"}), 200

    elif "pdf" in request.files:
        # If 'pdf' is in the uploaded files, it's a PDF
        pdf_file = request.files["pdf"]

        # Check if a PDF file is actually provided
        if pdf_file and pdf_file.filename.endswith(".pdf"):
            pdf_text = extract_text_from_pdf(pdf_file)
            Script_TEXT = pdf_text
            # print("Extracted text from PDF:", pdf_text)

            # Handle PDF text processing logic here

            # Return a success message
        
        
    tmp_file = tempfile.mkstemp()[1]
    with open(tmp_file, 'w') as f:
        f.write(script_text)
    upload_success = upload_file_to_s3(tmp_file, "hackllama")
    os.remove(tmp_file)
    if upload_success:
        print("text uploaded successfully.")
    else:
        print("text to upload video.")

    return jsonify({"error": "Invalid request"}), 400


def extract_text_from_pdf(pdf_file):
    # Use PyPDF2 or any other library to extract text from the PDF
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
        object_name = str(random.randint(10000, 99999))+os.path.basename(file_path)

    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return False
    return True



if __name__ == "__main__":
    app.run(debug=True, port=5003)

import json
from flask import Flask, request, redirect, url_for, render_template, jsonify
import os
import subprocess
import sys
import PyPDF2
import boto3
import random
import tempfile

from input_processing import extract_text_from_pdf, upload_file_to_s3, upload_python_object_to_s3

s3_client = boto3.client("s3")
from get_statistics import get_statistics

global Script_TEXT
Script_TEXT = ""

app = Flask(__name__)


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

        mp3_path = os.path.join(video_dir, "extracted_audio.mp3")
        subprocess.run(
            ["ffmpeg", "-y", "-i", temp_video_path, "-q:a", "0", "-map", "a", mp3_path]
        )

        os.remove(temp_video_path)
    return redirect(url_for("results"))


@app.route("/results")
def results():
    global Script_TEXT
    data = get_statistics(Script_TEXT)
    upload_python_object_to_s3(data, "hackllama", "statistics_data.json")
    print("Hallooooooooo")
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


if __name__ == "__main__":
    app.run(debug=True, port=5003)

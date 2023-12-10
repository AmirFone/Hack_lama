from flask import Flask, request, redirect, url_for, render_template, jsonify
import os
from moviepy.editor import VideoFileClip
import subprocess
from speech_to_text import extract_word_probabilities, transcribe_audio
import facial_expressions
from input_processing import extract_and_save_frames


app = Flask(__name__)
users = {"user": "password", "username": "password"}


@app.route("/")
def home():
    return render_template("index.html")  # Render the sign-in page


@app.route("/video", methods=["POST"])
def upload_video():
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

        # Extract audio as MP3
        mp3_path = os.path.join(video_dir, "extracted_audio.mp3")
        subprocess.run(
            ["ffmpeg", "-y", "-i", temp_video_path, "-q:a", "0", "-map", "a", mp3_path]
        )

        transcribed_data = transcribe_audio(mp3_path)
        # transcribed_word_timings = extract_word_timings(transcribed_data)
        transcribed_word_clarity = extract_word_probabilities(
            transcribed_data, probabilities_only=False
        )
        print(transcribed_word_clarity)

        # Optionally, remove the temporary webm file
        os.remove(temp_video_path)
        # Return success message
        return jsonify({"message": "Video and audio uploaded successfully"}), 200


    file_paths = extract_and_save_frames(
        video_path="demo_video.mp4", word_timings=transcribed_word_timings
    )
    video_analysis, eye_engagement = facial_expressions.process_images(file_paths)
    print(video_analysis, eye_engagement)
    
    
    
    return jsonify({"error": "Invalid request"}), 400



@app.route("/text", methods=["POST"])
def process_text_or_pdf():
    if "text" in request.form:
        # If 'text' is in the form data, it's text
        text = request.form["text"]

        # Handle text processing logic here
        print("Received text:", text)

        # Return a success message
        return jsonify({"message": "Text received and processed successfully"}), 200

    elif "pdf" in request.files:
        # If 'pdf' is in the uploaded files, it's a PDF
        pdf_file = request.files["pdf"]

        # Check if a PDF file is actually provided
        if pdf_file and pdf_file.filename.endswith(".pdf"):
            pdf_text = extract_text_from_pdf(pdf_file)
            print("Extracted text from PDF:", pdf_text)

            # Handle PDF text processing logic here

            # Return a success message
            return jsonify({"message": "PDF received and processed successfully"}), 200

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


if __name__ == "__main__":
    app.run(debug=True, port=5003)

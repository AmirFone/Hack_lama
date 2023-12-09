from flask import Flask, request, redirect, url_for, render_template, jsonify
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)
users = {"user": "password", "username": "password"}


@app.route("/")
def home():
    return render_template("index.html")  # Render the sign-in page


# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']
#     if username in users and users[username] == password:
#         return redirect(url_for('authenticated'))
#     return redirect(url_for('home'))

# @app.route('/authenticated')
# def authenticated():
#     return render_template('demo_upload.html')  # Render the authenticated page

# @app.route('/video', methods=['POST'])
# def upload_video():
#     if 'video' not in request.files:
#         return jsonify({"error": "No video part"}), 400

#     video = request.files['video']

#     if video.filename == '':
#         return jsonify({"error": "No selected video"}), 400

#     if video:  # If a video is actually present
#         video_path = os.path.join('.video', f'script_video.mp4')
#         video.save(video_path)

#         # we return our info
#         return jsonify({"message": "Video uploaded successfully"}), 200

#     return jsonify({"error": "Invalid request"}), 400


@app.route("/video", methods=["POST"])
def upload_video():
    global clip_counter
    if "video" not in request.files:
        return jsonify({"error": "No video part"}), 400

    video = request.files["video"]



    if video.filename == "":
        return jsonify({"error": "No selected video"}), 400
    

    if video:  # If a video is actually present
        
        
        video_dir = ".video"
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)
        # Save the original video
        video_path = os.path.join(".video", f"script_video.mp4")
        video.save(video_path)

        # Load the video file
        clip = VideoFileClip(video_path)

        # Extract audio from the video
        
        audio_dir = ".audio"
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)
        audio_path = os.path.join(".audio", f"script_audio.mp3")
        clip.audio.write_audiofile(audio_path)

        # Return success message
        return jsonify({"message": "Video and audio uploaded successfully"}), 200

    return jsonify({"error": "Invalid request"}), 400

@app.route('/text', methods=['POST'])
def process_text_or_pdf():
    if 'text' in request.form:
        # If 'text' is in the form data, it's text
        text = request.form['text']

        # Handle text processing logic here
        print("Received text:", text)

        # Return a success message
        return jsonify({"message": "Text received and processed successfully"}), 200

    elif 'pdf' in request.files:
        # If 'pdf' is in the uploaded files, it's a PDF
        pdf_file = request.files['pdf']

        # Check if a PDF file is actually provided
        if pdf_file and pdf_file.filename.endswith('.pdf'):
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
    app.run(debug=True)

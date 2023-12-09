from flask import Flask, request, redirect, url_for, render_template, jsonify
import os
from moviepy.editor import VideoFileClip
import subprocess

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

        # Optionally, remove the temporary webm file
        os.remove(temp_video_path)
        # Return success message
        return jsonify({"message": "Video and audio uploaded successfully"}), 200

    return jsonify({"error": "Invalid request"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5003)

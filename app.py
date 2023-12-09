from flask import Flask, request, redirect, url_for, render_template, jsonify
import os

app = Flask(__name__)
# users = {"user": "password", "username": "password"}

@app.route('/')
def home():
    return render_template('index.html')  # Render the sign-in page

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

@app.route('/video', methods=['POST'])
def upload_video():
    global clip_counter
    if 'video' not in request.files:
        return jsonify({"error": "No video part"}), 400

    video = request.files['video']

    if video.filename == '':
        return jsonify({"error": "No selected video"}), 400

    if video:  # If a video is actually present
        clip_counter += 1

        # Save the original video
        video_path = os.path.join('.video', f'script_video.mp4')
        video.save(video_path)

        # Load the video file
        clip = VideoFileClip(video_path)

        # Extract audio from the video
        audio_path = os.path.join('.audio', f'script_audio.mp3')
        clip.audio.write_audiofile(audio_path)

        # Return success message
        return jsonify({"message": "Video and audio uploaded successfully"}), 200

    return jsonify({"error": "Invalid request"}), 400



if __name__ == '__main__':
    app.run(debug=True)

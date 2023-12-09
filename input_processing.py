import os
import shutil
import cv2
import math


def extract_and_save_frames(video_path, word_timings, output_folder=".still_frames"):
    # Delete the output folder if it exists
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # Create the output folder
    os.makedirs(output_folder)

    # Calculate average timestamps
    timestamps = [(start + end) / 2 for _, start, end in word_timings]

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Get frames per second of the video

    for i, timestamp in enumerate(timestamps):
        frame_number = math.floor(timestamp * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            # Save the frame as a JPG file
            frame_path = os.path.join(output_folder, f"frame_{i}.jpg")
            cv2.imwrite(frame_path, frame)

    cap.release()

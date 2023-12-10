import os
import shutil
import cv2
import math
import json
import os
import PyPDF2
import boto3
import random
import tempfile

s3_client = boto3.client("s3")


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
    frame_paths = []
    for i, timestamp in enumerate(timestamps):
        frame_number = math.floor(timestamp * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            # Save the frame as a JPG file
            frame_path = os.path.join(output_folder, f"frame_{i}.jpg")
            frame_paths.append(frame_path)
            cv2.imwrite(frame_path, frame)

    cap.release()
    return frame_paths


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
        with open(tmp_file, "w") as f:
            json.dump(obj, f)
        upload_success = upload_file_to_s3(tmp_file, bucket_name, object_name)
        os.remove(tmp_file)
        return upload_success
    except Exception as e:
        print(f"Error uploading Python object to S3: {e}")
        return False

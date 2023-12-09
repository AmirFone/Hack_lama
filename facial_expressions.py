import base64
from collections import Counter
import requests

api_key = "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"


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def annotate_image(image_path):
    base64_image = encode_image(image_path)
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    text_prompt = """You are a helpful agent doing classification tasks. Given an image, 
                      Output the following about this image in the format (emotion, gaze_direction). 
                      The gaze direction should be in the form: center, left, right, up, or down. 
                      Select only ONE single most probable emotion and gaze direction.
                      DO NOT OUTPUT ANYTHING OTHER THAN A STRING IN THE FORM:
                      (emotion, gaze_direction) """
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text_prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    return response.json()


def process_images(images):
    video_analysis = []
    # eye_engagement = 0
    for image in images[:5]:  # TODO: This should be removed when we need one image analysis per word
        response = annotate_image(image)
        content = response["choices"][0]["message"]["content"]
        content = content[1:-1].split(",")
        sentiment, direction = content[0].strip(), content[1].strip()
        # if direction == 'center':
        #    eye_engagement += 1
        video_analysis.append((image, sentiment, direction))
    return video_analysis  # , eye_engagement/len(images)


def get_image_statistics(data):
    directions = [direction for _, _, direction in data]
    emotions = [emotion for _, emotion, _ in data]

    # Count occurrences
    direction_counts = Counter(directions)
    emotion_counts = Counter(emotions)

    # Calculate percentages
    total = len(data)
    direction_percentages = {k: (v / total) * 100 for k, v in direction_counts.items()}
    emotion_percentages = {k: (v / total) * 100 for k, v in emotion_counts.items()}

    # Determine average (mode)
    average_direction = max(direction_counts, key=direction_counts.get)
    average_emotion = max(emotion_counts, key=emotion_counts.get)

    return (
        direction_percentages,
        emotion_percentages,
        average_direction,
        average_emotion,
    )

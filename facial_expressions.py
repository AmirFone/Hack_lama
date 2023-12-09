import base64
import requests
import pdb

api_key = "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"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def annotate_image(image_path):
    base64_image = encode_image(image_path)
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }
    text_prompt =  """You are a helpful agent doing classification tasks. Given an image, 
                      Output the following about this image in the format (emotion, gaze_direction). 
                      The gaze direction should be in the form: center, left, right, up, or down. 
                      Select only ONE single most probable emotion and gaze direction.
                      DO NOT OUTPUT ANYTHING OTHER THAN A STRING IN THE FORM:
                      '(emotion, gaze_direction)' """
    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": text_prompt
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json())
    return response.json()


def process_images(images):
    video_analysis = []
    eye_engagement = 0
    for image in images:
        response = annotate_image(image)
        content = response['choices'][0]['message']['content']
        content = content[1:-1].split(",")
        sentiment, direction = content[0].strip(), content[1].strip()
        if direction == 'center':
           eye_engagement += 1
        video_analysis.append((image, sentiment, direction))
    return video_analysis, eye_engagement/len(images)

def main():
    video_analysis, engagement = process_images(['test1.jpg', 'test2.jpg', 'test3.jpg']) 
    print(video_analysis)
    print(engagement)
    return

if __name__ == "__main__":
    main()
  
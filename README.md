# Script AI

## Overview
Script AI is an innovative tool designed to enhance public speaking and acting performances. Utilizing the power of artificial intelligence, Script AI provides real-time feedback on speech delivery by analyzing video recordings. Ideal for actors and public speakers, this tool refines your presentation skills for maximum audience impact.

## Features

- **Video Recording**: Capture your performance directly through the platform for analysis.
- **Speech Analysis**: Advanced algorithms offer feedback on speech clarity, tempo, and emotion.
- **Script Processing**: Input scripts via text or upload PDFs for seamless integration.
- **Real-time Feedback**: Gain insights on improving delivery, tone, and audience engagement.
- **User-friendly Interface**: Navigate through the recording and analysis process with ease.

## Technical Stack
- **Frontend**: Crafted with modern web technologies for a responsive user experience.
- **Backend**: Built on Flask, our robust backend handles complex audio and video processing tasks efficiently.
- **Data Storage**: Utilizes AWS S3 for secure and scalable storage of video and script data.
- **Machine Learning**: Employs GPT Vision for facial expression analysis and Together API for generating the feedback.

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.6 or later
- Flask
- boto3
- openai-whisper (for audio analysis)
- All dependencies in `requirements.txt`

### Installation

1. Clone the repository:
     git clone <repository-url>
2. Install dependencies:
     pip install -r requirements.txt
3. Configure AWS and OpenAI credentials in your environment or `.env` file.

### Running the Application

Execute the following command:
Then, visit `http://localhost:5003` in your browser.

## Usage

### Uploading Your Script

- **Text**: Paste script text on the homepage.
- **PDF**: Drag and drop or select a PDF script file.

### Recording Your Performance

Hit the record button post-upload and grant browser camera and microphone access.

### Receiving Feedback

Post-performance, Script AI processes the video and audio, providing detailed speech insights.

## Screenshots

Here's Script AI in action:
![ezgif com-video-to-gif (3)](https://github.com/AmirFone/Hack_lama/assets/93888864/1218e171-2cf1-4cb7-990f-84cb3d498773)
![Script Analysis Results](https://github.com/AmirFone/Hack_lama/assets/93888864/79ed6ebb-234f-4f10-94b3-80a6e91aeb2b.png)
![Script AI Logo](https://github.com/AmirFone/Hack_lama/assets/93888864/71a3cd9c-6aa9-4d66-8a93-74e345f4acea.png)
![Feedback Interface](https://github.com/AmirFone/Hack_lama/assets/93888864/452afa9d-f53f-4b1d-83b9-945351f22fa5.png)

## Contributions

We welcome contributions! Feel free to submit pull requests or open issues for discussion.

## License

Script AI is released under the [MIT License](LICENSE).


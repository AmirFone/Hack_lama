import whisper

def transcribe_audio(filename):
    model = whisper.load_model("medium")

    result = model.transcribe(
        audio=filename,
        fp16=False,
    )
    return result["text"]

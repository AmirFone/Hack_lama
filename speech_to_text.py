import whisper


def transcribe_audio(filename):
    model = whisper.load_model("medium")

    result = model.transcribe(
        audio=filename,
        fp16=False,
        initial_prompt="Transcribe the audio, in your transcription, add '[pause]' for every pause.",
        word_timestamps=True,
    )

    return result


def extract_word_timings(input_dict):
    word_timings = []

    # Iterate through each segment
    for segment in input_dict["segments"]:
        # Iterate through each word in the segment
        for word_info in segment["words"]:
            word = word_info["word"]
            start = word_info["start"]
            end = word_info["end"]

            # Append the tuple (word, start, end) to the list
            word_timings.append((word, start, end))

    return word_timings


def chain_words_with_pauses(word_data, pause_length_seconds):
    chained_text = ""
    prev_end = 0  # Initialize previous end time to 0
    first_word = True  # Flag to check if it's the first word

    for word, start, end in word_data:
        # Check if the pause is needed and it's not the first word
        if start - prev_end > pause_length_seconds and not first_word:
            chained_text += " [pause]"

        chained_text += word
        prev_end = end  # Update the end time for the next iteration
        first_word = False  # Update the flag after the first word is processed

    return chained_text

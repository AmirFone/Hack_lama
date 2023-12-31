import whisper


def transcribe_audio(filename):
    model = whisper.load_model("tiny")  # "base"

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


def extract_word_probabilities(input_dict, probabilities_only=False):
    output = []

    # Iterate through each segment
    for segment in input_dict["segments"]:
        # Iterate through each word in the segment
        for word_info in segment["words"]:
            word = word_info["word"]
            probability = word_info["probability"]

            # Append the tuple (word, probability) or just the probability
            if probabilities_only:
                output.append(probability)
            else:
                output.append((word, probability))

    return output


def calculate_word_times(word_times_list):
    times_per_word = []
    times_per_word_length = []

    for word, start, end in word_times_list:
        duration = end - start
        times_per_word.append((word, duration))

        # Calculate time per character, excluding spaces and punctuation
        word_length = len(word.strip().strip(".,!?"))
        if word_length > 0:
            time_per_char = duration / word_length
        else:
            time_per_char = 0
        times_per_word_length.append((word, time_per_char))

    return times_per_word, times_per_word_length


def analyze_pause_alignment(string1, string2):
    # Convert strings to lists of words
    words1 = string1.split()
    words2 = string2.split()

    # Count total pauses in both strings
    total_pauses = words1.count("[pause]") + words2.count("[pause]")

    # If there are no pauses in both strings, return 1 as they are perfectly aligned in terms of pauses
    if total_pauses == 0:
        return 1

    # Count matching pauses
    matching_pauses = 0
    for w1, w2 in zip(words1, words2):
        if w1 == "[pause]" and w2 == "[pause]":
            matching_pauses += 1

    # Calculate the score
    score = matching_pauses / (total_pauses / 2)
    return score

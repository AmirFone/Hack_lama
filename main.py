from input_processing import extract_and_save_frames
from script_correctness import analyze_correctness
from speech_to_text import (
    chain_words_with_pauses,
    extract_word_probabilities,
    extract_word_timings,
    transcribe_audio,
)
import facial_expressions

if __name__ == "__main__":
    transcribed_data = transcribe_audio("demo_video.mp3")

    transcribed_word_timings = extract_word_timings(transcribed_data)
    transcribed_word_clarity = extract_word_probabilities(
        transcribed_data, probabilities_only=True
    )
    print(transcribed_word_clarity)

    file_paths = extract_and_save_frames(
        video_path="demo_video.mp4", word_timings=transcribed_word_timings
    )
    video_analysis, eye_engagement = facial_expressions.process_images(file_paths)
    
    transcribed_text_with_pauses = chain_words_with_pauses(
        word_data=transcribed_word_timings, pause_length_seconds=0.8
    )

    transcribed_text = transcribed_data["text"]

    script_correctness = analyze_correctness(
        spoken_text=transcribed_text,
        script_input="It's come down to this, hasn't it? [pause] All the roads I've taken, all the choices I've made. [pause] And yet, here I stand, at the crossroads of my destiny.",
    )

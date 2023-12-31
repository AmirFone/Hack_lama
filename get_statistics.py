import os
import json
import subprocess
import facial_expressions
from feedback import llama_feedback
from input_processing import extract_and_save_frames
from script_correctness import analyze_correctness
from speech_to_text import (
    analyze_pause_alignment,
    calculate_word_times,
    chain_words_with_pauses,
    extract_word_probabilities,
    extract_word_timings,
    transcribe_audio,
)


def get_statistics(script):
    video_dir = ".video"

    mp4_path = os.path.join(video_dir, "converted_video.mp4")
    mp3_path = os.path.join(video_dir, "extracted_audio.mp3")

    transcribed_data = transcribe_audio(mp3_path)
    transcribed_text = transcribed_data["text"]

    transcribed_word_timings = extract_word_timings(transcribed_data)
    times_per_word, times_per_word_length = calculate_word_times(
        transcribed_word_timings
    )

    transcribed_text_with_pauses = chain_words_with_pauses(
        word_data=transcribed_word_timings, pause_length_seconds=0.8
    )
    num_pauses = transcribed_text_with_pauses.count("[pause]")
    pause_alignment_score = analyze_pause_alignment(
        script, transcribed_text_with_pauses
    )

    transcribed_word_clarity = extract_word_probabilities(
        transcribed_data, probabilities_only=False
    )
    average_word_clarity = (
        sum(value for _, value in transcribed_word_clarity)
        / len(transcribed_word_clarity)
        if len(transcribed_word_clarity) > 0
        else 1
    )  # Assumes probabilities_only=False

    script_correctness = analyze_correctness(
        spoken_text=transcribed_text_with_pauses,
        script_input=script,  # Assumes script has '[pause]' annotated
    )

    file_paths = extract_and_save_frames(
        video_path=mp4_path, word_timings=transcribed_word_timings
    )
    video_analysis = facial_expressions.process_images(file_paths)
    (
        direction_percentages,
        emotion_percentages,
        average_direction,
        average_emotion,
    ) = facial_expressions.get_image_statistics(data=video_analysis)

    statistics = {
        "transcribed_text": transcribed_text,
        "words_and_clarity_scores": transcribed_word_clarity,
        "average_clarity_score": average_word_clarity,
        "transcribed_word_timings": transcribed_word_timings,
        "transcribed_text_with_pauses": transcribed_text_with_pauses,
        "script_correctness_score": script_correctness,
        "direction_percentages": direction_percentages,
        "emotion_percentages": emotion_percentages,
        "average_direction": average_direction,
        "average_emotion": average_emotion,
        "num_pauses": num_pauses,
        "pause_alignment_score": pause_alignment_score,
        "times_per_word": times_per_word,
        "times_per_word_length": times_per_word_length,
    }
    
    reduced_stats = {
        "average_clarity_score": average_word_clarity,
        "transcribed_text_with_pauses": transcribed_text_with_pauses,
        "script_correctness_score": script_correctness,
        "direction_percentages": direction_percentages,
        "emotion_percentages": emotion_percentages,
        "average_direction": average_direction,
        "average_emotion": average_emotion,
        "num_pauses": num_pauses,
        "pause_alignment_score": pause_alignment_score,
        "times_per_word_length": times_per_word_length,
    }    
    
    feedback = llama_feedback(json.dumps(reduced_stats, indent=4)).replace("\n", "")
    statistics["feedback"] = feedback

    return statistics

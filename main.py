from script_correctness import analyze_correctness
from speech_to_text import (
    chain_words_with_pauses,
    extract_word_timings,
    transcribe_audio,
)


if __name__ == "__main__":
    transcribed_data = transcribe_audio("sample_script.mp3")

    transcribed_word_timings = extract_word_timings(transcribed_data)
    # print(transcribed_word_timings)
    transcribed_text_with_pauses = chain_words_with_pauses(
        word_data=transcribed_word_timings, pause_length_seconds=0.8
    )
    print(transcribed_text_with_pauses)

    # transcribed_text = transcribed_data["text"]
    # # print(transcribed_text)

    # print(
    #     analyze_correctness(
    #         spoken_text=transcribed_text,
    #         script_input="It's come down to this, hasn't it? [pause] All the roads I've taken, all the choices I've made. [pause] And yet, here I stand, at the crossroads of my destiny.",
    #     )
    # )

import difflib


def analyze_correctness(spoken_text, script_input):
    sequence_matcher = difflib.SequenceMatcher(None, spoken_text, script_input)
    return sequence_matcher.ratio()

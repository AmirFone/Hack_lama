import requests


def llama_feedback(data=None):
    prompt = """
            Given the data below about an aspiring actor who is practicing a script, find some 
            key insights and return me a two sentence analysis. Don't say anything about the 
            script, just give feedback on the tonality and the perceived attention from the data 
            and how well a person performed the script. Context:
            """
    if data is None:
        data = "generate a two sentence script for me to present to an audience"
    else:
        data = prompt + data

    endpoint = "https://api.together.xyz/inference"

    res = requests.post(
        endpoint,
        json={
            "model": "togethercomputer/llama-2-70b-chat",
            "max_tokens": 80,
            "prompt": data,
            "request_type": "language-model-inference",
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1,
            "stop": ["</s>"],
            "negative_prompt": "",
            "sessionKey": "6232361f5cf7cbc564512bc8a99396e7cf6f8445",
            "type": "language",
        },
        headers={
            "Authorization": "Bearer 2f4d0f5a97955ba793b6b8dac50f2f0f2f834dc9863ade1d9feef1769c2b15ee",
        },
    )
    return res.json()["output"]["choices"][0]["text"]

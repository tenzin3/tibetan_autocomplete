import os
from anthropic import Anthropic
from typing import Literal

def get_api_key() -> str:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
    return os.environ.get("ANTHROPIC_API_KEY")

def get_client():
    api_key = get_api_key()
    return Anthropic(api_key=api_key)

def get_completion(client: Anthropic, tibetan_text: str)->str:
    prompt = f"""
            Complete this Tibetan sentence with the single most natural and 
            commonly used ending words or particles: {tibetan_text}
            This revised prompt:
            1. Specifies that you want only the single most natural completion
            2. Clarifies you're looking for just the ending words/particles (not multiple options)
            3. Maintains context that this is a Tibetan sentence
            4. Eliminates the possibility of getting explanations about the phrase
            5. Dont include the input text in the output
    """
    
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="claude-3-5-sonnet-latest",
    )

    completion_text = message.content[0].text
    return completion_text

def get_english_completion(client: Anthropic, english_text: str)->str:
    prompt = f"""
            Complete this English sentence with the single most natural and 
            commonly used ending words or particles: {english_text}
            This revised prompt:
            1. Specifies that you want only the single most natural completion
            2. Clarifies you're looking for just the ending words/particles (not multiple options)
            3. Maintains context that this is an English sentence
            4. Eliminates the possibility of getting explanations about the phrase
            5. Dont include the input text in the output
    """
    
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="claude-3-5-sonnet-latest",
    )

    completion_text = message.content[0].text
    return completion_text

def main(input_text: str, language: Literal["tibetan", "english"] = "english") -> str:
    client = get_client()
    if language == "tibetan":
        return get_completion(client, input_text)
    else:
        return get_english_completion(client, input_text)

if __name__ == "__main__":

    # Test English completion
    english_text = "The quick brown fox jumps over"
    english_completion = main(english_text)
    print(f"English completion: {english_completion}")
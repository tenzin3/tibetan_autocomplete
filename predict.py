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

def get_llm_response(client: Anthropic, prompt: str)->str:
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

def get_tibetan_completion(client: Anthropic, tibetan_text: str)->str:
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
    
    return get_llm_response(client, prompt)

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
    return get_llm_response(client, prompt)

def is_gibberish(client: Anthropic, text: str, language: Literal["tibetan", "english"] = "english") -> bool:
    """Check if the given text is gibberish using LLM.
    
    Args:
        client: Anthropic client instance
        text: Text to check
        language: Language of the text ('tibetan' or 'english')
    
    Returns:
        bool: True if text is gibberish, False otherwise
    """
    prompt = f"""
    Analyze if the following {language} text is gibberish (meaningless, random characters, or nonsensical text) or not.
    Text: {text}
    
    Instructions:
    1. Consider the text's grammar, word combinations, and overall meaning
    2. For Tibetan text, check if it uses valid Tibetan syllables and grammar
    3. For English text, check if it uses valid English words and grammar
    4. Respond with ONLY 'true' if it's gibberish or 'false' if it's valid text
    5. Do not provide any explanation, just return 'true' or 'false'
    """
    
    response = get_llm_response(client, prompt).strip().lower()
    return response == 'true'

def main(input_text: str, language: Literal["tibetan", "english"] = "english") -> str:
    client = get_client()

    # If input text is empty, return empty string
    if not input_text.strip():
        return ""

    if is_gibberish(client, input_text, language):
        return ""

    if language == "tibetan":
        return get_tibetan_completion(client, input_text)
    else:
        return get_english_completion(client, input_text)

if __name__ == "__main__":
    client = get_client()


    # Test gibberish detection
    print("\nTesting gibberish detection:")
    
    # Test valid English
    valid_english = "The sky is blue today"
    print(f"Valid English: '{valid_english}' -> Is gibberish? {is_gibberish(client, valid_english, 'english')}")
    
    # Test gibberish English
    gibberish_english = "asdf qwerty blorp zxcv"
    print(f"Gibberish English: '{gibberish_english}' -> Is gibberish? {is_gibberish(client, gibberish_english, 'english')}")
    
    # Test valid Tibetan
    valid_tibetan = "ང་སྐྱིད་པོ་"
    print(f"Valid Tibetan: '{valid_tibetan}' -> Is gibberish? {is_gibberish(client, valid_tibetan, 'tibetan')}")
    
    # Test gibberish Tibetan
    gibberish_tibetan = "ཨཨཨ་པཔཔ་སསས་"
    print(f"Gibberish Tibetan: '{gibberish_tibetan}' -> Is gibberish? {is_gibberish(client, gibberish_tibetan, 'tibetan')}")
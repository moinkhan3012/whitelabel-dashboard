import requests
import re
import string
import streamlit as st
from collections import defaultdict
from nltk.tokenize import word_tokenize


def get_all_contexts(text, target_word, context_size=5):
    """
    Extracts all contexts of a target word in a text.

    Args:
        text (str): The input text to search within.
        target_word (str): The word to find contexts for.
        context_size (int): Number of words before and after the target word. Defaults to 5.

    Returns:
        list: List of context strings.
    """
    # Clean the text and tokenize it
    tokens = word_tokenize(re.sub('[^a-zA-Z0-9 ]+', '', text))
    tokens = [token for token in tokens if token not in string.punctuation]

    # Find all occurrences of the target word
    target_indices = [i for i, token in enumerate(tokens) if token.lower() == target_word.lower()]

    # Extract context sentences for each occurrence of the target word
    all_contexts = []
    for target_index in target_indices:
        start_index = max(0, target_index - context_size)
        end_index = min(len(tokens), target_index + context_size + 1)
        context_words = tokens[start_index:end_index]
        context_sentence = ' '.join(context_words)
        all_contexts.append(context_sentence)

    return all_contexts


def __extract_app_name(text):
    """
    Extracts app names from a given text using a SpaCy NER model on Hugging Face.

    Args:
        text (str): The input text to extract from.

    Returns:
        dict: Dictionary with "apps" key listing extracted app names or "err" key in case of an error.
    """
    # Fetch API credentials from Streamlit secrets
    API_URL = st.secrets.huggingface_cred.API_URL_SPACY
    API_TOKEN = st.secrets.huggingface_cred.API_TOKEN
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    payload = {
        "inputs": text,
        "options": {
            "wait_for_model": True  # Avoid 503 issue
        }
    }

    # Make the API request
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return {"apps": [app['word'] for app in response.json()]}
 
    return {"err": response.json()['error']}


def get_app_name(text):
    """
    Extracts the most frequently occurring app name from a text.

    Args:
        text (str): The input text.

    Returns:
        dict: Dictionary with "app" key listing the app name or "err" key in case of an error.
    """
    # Get contexts containing the word "app"
    contexts = get_all_contexts(text, "app")

    app_name = defaultdict(int)

    for context in contexts:
        result = __extract_app_name(context)
        if 'err' in result:
            st.warning(f"Could not complete inference! {result['err']}", icon="⚠️")
            return {'err': result['err']}
        
        # Count occurrences of each app name
        for app in result['apps']:
            name = re.sub("[^a-zA-Z0-9]", "", app.upper())
            app_name[name] += 1

    # Return the most frequently occurring app name or None
    return {'app': max(app_name, key=app_name.get) if app_name else None}
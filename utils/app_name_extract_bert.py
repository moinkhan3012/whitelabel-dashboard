import string
import re
import requests
from nltk import word_tokenize
import streamlit as st
from fuzzywuzzy import fuzz


def are_similar(s1, s2, threshold=50):
    """
    Check if two strings are similar based on a fuzzy match threshold.

    Args:
        s1 (str): First string to compare.
        s2 (str): Second string to compare.
        threshold (int): Similarity threshold. Defaults to 50.

    Returns:
        bool: True if the strings are similar, False otherwise.
    """
    return fuzz.token_sort_ratio(s1.lower().replace(' ', ''), s2.lower().replace(' ', '')) >= threshold


def group_similar_strings(strings, threshold=50):
    """
    Group similar strings together based on a fuzzy match threshold.

    Args:
        strings (list): List of strings to group.
        threshold (int): Similarity threshold. Defaults to 50.

    Returns:
        list: List of groups of similar strings.
    """
    groups = []
    for string in strings:
        matched = False
        for group in groups:
            # Check if the string matches with any existing string in the group
            if any(are_similar(string, existing_str, threshold) for existing_str in group):
                group.append(string)
                matched = True
                break
        if not matched:
            groups.append([string])
    return groups


def get_all_contexts(text, target_word, context_size=5):
    """
    Extract all contexts of a target word in a text.

    Args:
        text (str): Text to search in.
        target_word (str): Word to find contexts for.
        context_size (int): Number of words before and after the target word. Defaults to 5.

    Returns:
        list: List of contexts as strings.
    """
    # Tokenize the text and clean it
    tokens = word_tokenize(re.sub('[^a-zA-Z0-9 ]+', '', text))
    tokens = [token for token in tokens if token not in string.punctuation]

    # Find all occurrences of the target word
    target_indices = [
        i for i, token in enumerate(tokens)
        if re.fullmatch('[a-zA-Z0-9]+', token) and token.lower() == target_word.lower()
    ]

    # Extract context sentences for each occurrence of the target word
    all_contexts = [
        ' '.join(tokens[max(0, i - context_size):min(len(tokens), i + context_size + 1)])
        for i in target_indices
    ]

    return all_contexts


def reconstruct_tokens(predictions, label_mapping):
    """
    Reconstruct tokens from BERT-style subword predictions.

    Args:
        predictions (list): List of token predictions.
        label_mapping (dict): Mapping from model labels to readable labels.

    Returns:
        list: List of reconstructed entities.
    """
    reconstructed_tokens = []
    current_word = []
    current_label = None

    for token in predictions:
        if token['word'].startswith('##'):
            # Handle subwords by removing '##' prefix and appending to the current word
            current_word.append(token['word'][2:])
        else:
            # If there's a current word, it's complete
            if current_word:
                reconstructed_word = ''.join(current_word)
                reconstructed_tokens.append({
                    'word': reconstructed_word,
                    'entity': label_mapping[current_label]
                })
                current_word = []
                current_label = None

            # Start a new word
            current_word.append(token['word'])
            current_label = token['entity']

    # Handle the last word if any
    if current_word:
        reconstructed_word = ''.join(current_word)
        reconstructed_tokens.append({
            'word': reconstructed_word,
            'entity': label_mapping[current_label]
        })

    # Combine 'B-APP' and 'I-APP' entities into single app names
    app_name = []
    for entity in reconstructed_tokens:
        if entity['entity'] == 'B-APP':
            app_name.append(entity['word'])
        elif app_name and entity['entity'] == 'I-APP':
            app_name[-1] += f" {entity['word']}"

    return app_name


def __extract_app_name(text):
    """
    Extract app names from text using a BERT NER model hosted on Hugging Face.

    Args:
        text (str): Input text to extract from.

    Returns:
        dict: Dictionary with "apps" key listing extracted app names or "err" key in case of an error.
    """
    label_mapping = {
        "LABEL_0": "O",
        "LABEL_1": "B-APP",
        "LABEL_2": "I-APP"
    }

    API_URL = st.secrets.huggingface_cred.API_URL_BERT
    API_TOKEN = st.secrets.huggingface_cred.API_TOKEN
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {
        "inputs": text,
        "parameters": {"aggregation_strategy": "none"},
        "options": {"wait_for_model": True}
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        app_names = reconstruct_tokens(response.json(), label_mapping)
        return {"apps": app_names}

    return {"err": response.json().get('error', 'Unknown error')}


def get_app_name(product):
    """
    Extract app names from a product description.

    Args:
        product (dict): Dictionary with "short_description" and "long_description" keys.

    Returns:
        dict: Dictionary with "app" key listing the app name or "err" key in case of an error.
    """
    app_names = []

    # Extract contexts containing the word "app" from both descriptions
    for text in [product['short_description'], product['long_description']]:
        contexts = get_all_contexts(text, 'app')
        for context in contexts:
            result = __extract_app_name(re.sub('[^a-zA-Z0-9 ]+', '', context))
            if 'err' in result:
                return {'err': result['err']}
            app_names.extend(result['apps'])

    # Group similar app names (e.g., "alfredcamera" and "alfredcam")
    if app_names:
        app_names = sorted(group_similar_strings(app_names, threshold=50), key=len, reverse=True)[0][0]

    return {'app': app_names}
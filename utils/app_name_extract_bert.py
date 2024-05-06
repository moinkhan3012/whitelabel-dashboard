from fuzzywuzzy import fuzz
import string
import re
import requests
import nltk 
from nltk import word_tokenize
import streamlit as st
nltk.download('punkt')


def are_similar(s1, s2, threshold=50):
    return fuzz.token_sort_ratio(s1.lower().replace(' ', ''), s2.lower().replace(' ', '')) >= threshold

def group_similar_strings(strings, threshold=50):
    groups = []
    for string in strings:
        matched = False
        for group in groups:
            if any(are_similar(string, existing_str, threshold) for existing_str in group):
                group.append(string)
                matched = True
                break
        if not matched:
            groups.append([string])
    return groups

def get_all_contexts(text, target_word, context_size=5):
    # Tokenize the text
    tokens = word_tokenize(re.sub('[^a-zA-Z0-9 ]+', '', text))
    
    tokens = [token for token in tokens if token not in string.punctuation]

    # Find all occurrences of the target word
    target_indices = []
    for i, token in enumerate(tokens):
        match  = re.findall('[a-zA-Z0-9]+', token)
        if match and match[0].lower() == target_word.lower():
            target_indices.append(i)

    # Extract context sentences for each occurrence of the target word
    all_contexts = []
    for target_index in target_indices:
        start_index = max(0, target_index - context_size)
        end_index = min(len(tokens), target_index + context_size + 1)
        context_words = tokens[start_index:end_index]
        context_sentence = ' '.join(context_words)
        all_contexts.append(context_sentence)

    return all_contexts


def reconstruct_tokens(predictions, label_mapping):
    reconstructed_tokens = []
    current_word = []
    current_label = None

    for token in predictions:
        if token['word'].startswith('##'):  # Handle subwords
            current_word.append(token['word'][2:])  # Remove '##' prefix
        else:
            if current_word:  # If there's a current word, it's complete
                reconstructed_word = ''.join(current_word)
                reconstructed_tokens.append({
                    'word': reconstructed_word,
                    'entity': label_mapping[current_label]
                })
                current_word = []
                current_label = None

            current_word.append(token['word'])
            current_label = token['entity']

    # Handle the last word if any
    if current_word:
        reconstructed_word = ''.join(current_word)
        reconstructed_tokens.append({
            'word': reconstructed_word,
            'entity': label_mapping[current_label]
        })

    print(reconstructed_tokens)

    app_name = []
    for entity in reconstructed_tokens:
        if entity['entity']=='B-APP':
            app_name.append(entity['word'])
        elif app_name and entity['entity']=='I-APP':
            app_name[-1] += f" {entity['word']}"

    return app_name


def __extract_app_name(text):
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
        "parameters": {"aggregation_strategy" : "none"},
        "options": {
            "wait_for_model": True #avoid 503 issue
        }
    }
    
    
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code ==200:
        app_names = reconstruct_tokens(response.json(), label_mapping)
        return {"apps": app_names}

    return {"err": response.json()['error']}



def get_app_name(product):

    app_names = []


    for text in [product['short_description'], product['long_description']]:
        # st.markdown(text)
        contexts = get_all_contexts(text, 'app')

        for context in contexts:   
            result = __extract_app_name(re.sub('[^a-zA-Z0-9 ]+', '', context))
            if 'err' in result:
                return {'err': result['err']}


            app_names.extend(result['apps'])
            

    if app_names:
        #group similar app names example alfredcamera, alfredcam
        app_names  = sorted(group_similar_strings(app_names, threshold=50), key=len, reverse=True)[0][0]

    return {'app': app_names}
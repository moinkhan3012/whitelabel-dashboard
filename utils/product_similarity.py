import requests
import re
import string
import streamlit as st
from collections import defaultdict
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

def get_all_contexts(text, target_word, context_size=5):
    # Tokenize the text
    tokens = word_tokenize(text)

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
    API_URL = st.secrets.huggingface_cred.API_URL
    API_TOKEN = st.secrets.huggingface_cred.API_TOKEN
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    payload = {
        "inputs": text,
        "options": {
            "wait_for_model": True #avoid 503 issue
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code ==200:
    	return {"apps": [app['word'] for app in response.json()]}

    return {"err": response.json()['error']}
    

def get_app_name(text):

    contexts = get_all_contexts(text, "app")

    app_name = defaultdict(int)

    for context in contexts:
        result = __extract_app_name(context)
        if 'err' in result:
            st.warning(f"Could not completed inference! {result['err']}", icon="⚠️")
            return
        
        #iterate through the entities
        for app in result['apps']:
            name = re.sub("[^a-zA-Z0-9]", "", app.upper())
            app_name[name]  +=1

    # return app_name if app_name else None
    return max(app_name, key=app_name.get) if app_name else None

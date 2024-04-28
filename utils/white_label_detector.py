import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from transformers import BertTokenizer, BertModel
import torch
import pandas as pd

import numpy as np
from transformers import BertTokenizer, BertModel
import torch.nn.functional as F
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from PIL import Image
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
nlp = spacy.load("en_core_web_sm")

import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from PIL import Image
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt


## Data Processing

df = pd.read_csv('/Users/priyankabose/Streamlit Dashboard/whitelabel-dashboard/amazon_smart_cameras_products_dataset - amazon_smart_cameras_products_dataset (1).csv')
df.columns

## Extract App Names

# NER

# nltk.data.path.append(r".\tokenizers")
nltk.download('punkt')
#load the model
# nlp = spacy.load(r"C:\Users\moink\Downloads\white_label\model-best")
nlp = spacy.load(r"/Users/priyankabose/Desktop/case_sensitive_ner")

import string
from collections import defaultdict
import re

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

def get_app_name(nlp, text):

    contexts = get_all_contexts(text, "app")

    app_name = defaultdict(int)

    for context in contexts:
        doc = nlp(context)

        #iterate through the entities
        for ent in doc.ents:
            name = re.sub("[^a-zA-Z0-9]", "", ent.text.upper())
            app_name[name]  +=1

    # return app_name if app_name else None
    return max(app_name, key=app_name.get) if app_name else None


for index, row in df.iterrows():
#download punkt using nltk.download('punkt') and provide the path below

    description_list = [row['long_description'] , row['short_description']]



    app_name = None
    row['app_name'] = None
    for description in description_list:

        if description:
            app_name = get_app_name(nlp, description.replace("\n", " "))

    df.at[index, 'app_name'] = app_name
    print(df.at[index, 'app_name'])

df['app_name'].isna().sum()
df[(df['app_name'].notnull()) & (df['app_name']=='24H')]
df[df['id']=='B0CN38Z8WP']

nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [stemmer.stem(token) for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(tokens)

df['processed_long_description'] = df['long_description'].apply(preprocess_text)
df = df.rename({'processed_long_description': 'long_description'})

# Model Building

# Text Similarity: TFIDF

# Calculate similarity scores based on 'short_description' and 'long_description'
short_desc_vectorizer = TfidfVectorizer()
short_desc_matrix_tfidf = short_desc_vectorizer.fit_transform(df['short_description'].apply(preprocess_text))

long_desc_vectorizer = TfidfVectorizer()
long_desc_matrix_tfidf = long_desc_vectorizer.fit_transform(df['long_description'].apply(preprocess_text))

# Cosine similarity for short descriptions
short_desc_similarity_matrix_tfidf = cosine_similarity(short_desc_matrix_tfidf, dense_output=False)

# Cosine similarity for long descriptions
long_desc_similarity_matrix_tfidf = cosine_similarity(long_desc_matrix_tfidf, dense_output=False)

short_desc_matrix_tfidf.shape

# Image Similarity: RestNet50

base_model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

images_dir = "/Users/priyankabose/Desktop/Smart Cameras"
image_paths = [os.path.join(images_dir, img) for img in sorted(os.listdir(images_dir)) if img.endswith(('.png', '.jpg', '.jpeg'))]

def extract_features(img_path):
    img = Image.open(img_path)
    img = img.resize((224, 224))  # Resize image to the input size expected by ResNet-50
    img_array = np.array(img)
    img_array = preprocess_input(img_array)  # Preprocess input according to ResNet-50 requirements
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    features = base_model.predict(img_array, verbose=None)
    return features.flatten()

print("extracting features")
# Extract features from each image
feature_matrix = np.array([extract_features(img_path) for img_path in image_paths])

img_similarity_matrix = cosine_similarity(feature_matrix)
image_paths_id = [path.rsplit('/')[-1].split('_')[0] for path in image_paths]
image_paths_id.index('B01BHQ1IQK')

# TFIDF Text X Image Resent Similarity Matrix
product_matrix_df = pd.DataFrame()
for i in range(len(df)):
    id1 = df.iloc[i]['id']
    image_1_index = image_paths_id.index(id1)
    for j in range(i+1, len(df)):
        id2 = df.iloc[j]['id']
        image_2_index = image_paths_id.index(id2)
        temp_df = pd.DataFrame([{'product_1': id1, 'product_2': id2, 'brand_1': df.iloc[i]['brand'], 'brand_2': df.iloc[j]['brand'], 'text_short': short_desc_similarity_matrix_tfidf[i, j], 'text_long': long_desc_similarity_matrix_tfidf[i,j], 'image': img_similarity_matrix[image_1_index][image_2_index], 'product_1_url': df.iloc[i]['url'], 'product_2_url': df.iloc[j]['url']}])
        product_matrix_df = pd.concat([temp_df, product_matrix_df], ignore_index=True)

product_matrix_df.to_csv("/Users/priyankabose/Streamlit Dashboard/whitelabel-dashboard/amazon_smart_cameras_products_text_image_matrix_tfidf.csv", index=False)

product_matrix_df.sort_values('image', ascending=False).head()

product_matrix_df.sort_values('image', ascending=False).head()

product_matrix_df['product_2_url'][14896]




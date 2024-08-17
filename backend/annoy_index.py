import os
import numpy as np
from annoy import AnnoyIndex
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import pandas as pd


#one time thing, should be saved into the database as read only, unless we expand with more datasets
def create_feature_matrix(df):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['categories'])
    
    scaler = MinMaxScaler()
    numerical_features = scaler.fit_transform(df[['review_count', 'rating', 'latitude', 'longitude']].fillna(0))
    
    price_dummies = pd.get_dummies(df['price'], prefix='price').fillna(0)
    
    features = np.hstack((tfidf_matrix.toarray(), numerical_features, price_dummies.values))
    
    return features, tfidf, scaler


def build_annoy_index(features, n_trees=5, max_items=100):
    print(f"Building Annoy index with {features.shape[1]} dimensions...")
    f = features.shape[1]
    t = AnnoyIndex(f, 'angular')
    try:
        for i in range(min(features.shape[0], max_items)):
            print(f"Adding item {i} to the index")
            t.add_item(i, features[i])
        print(f"Added {min(features.shape[0], max_items)} items to the index")
        
        print(f"Starting to build index with {n_trees} trees...")
        t.build(n_trees)
        print(f"Built index with {n_trees} trees")
    except Exception as e:
        print(f"Error in build_annoy_index: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    return t

def create_and_save_annoy_index(df, file_path='datasets/item_similarity.ann'):
    features, tfidf, scaler = create_feature_matrix(df)
    
    if not os.path.exists(file_path):
        print(f"Annoy index file '{file_path}' not found. Building a new one...")
        annoy_index = build_annoy_index(features)
        try:
            annoy_index.save(file_path)
            print(f"Annoy index saved successfully at {file_path}")
        except Exception as e:
            print(f"Error saving Annoy index: {str(e)}")
    else:
        print(f"Annoy index file '{file_path}' found. Loading the existing index...")
        annoy_index = AnnoyIndex(features.shape[1], 'angular')
        annoy_index.load(file_path)
        print(f"Annoy index loaded successfully from {file_path}")
    
    return features, tfidf, scaler

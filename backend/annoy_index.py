import os
import numpy as np
from annoy import AnnoyIndex
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

def create_feature_matrix(df):
    tfidf = TfidfVectorizer(tokenizer=lambda x: x.split('||'))
    df['processed_categories'] = df['categories'].apply(lambda x: x.replace(', ', '||'))

    tfidf_matrix = tfidf.fit_transform(df['processed_categories'])
    scaler = MinMaxScaler()
    numerical_features = scaler.fit_transform(df[['review_count', 'rating']].fillna(0))
    
    price_dummies = pd.get_dummies(df['price'], prefix='price').fillna(0)
    
    features = np.hstack((tfidf_matrix.toarray(), numerical_features, price_dummies.values))
    # print('\n\nshape:',features.shape)
    return features, tfidf, scaler

def build_annoy_index(features, n_trees=150):
    # print(f"Building Annoy index with {features.shape[1]} dimensions...")
    f = features.shape[1]
    t = AnnoyIndex(f, 'angular')
    try:
        for i in range(features.shape[0]):
            print(f"Adding item {i} to the index")
            t.add_item(i, features[i])
        print(f"Added {features.shape[0]} items to the index")
        
        print(f"Starting to build index with {n_trees} trees...")
        t.build(n_trees)
        print(f"Built index with {n_trees} trees")
    except Exception as e:
        print(f"Error in build_annoy_index: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    return t

def is_valid_annoy_file(file_path, num_dimensions):
    """Check if the Annoy index file is valid by attempting to load it and checking the number of items."""
    try:
        index = AnnoyIndex(num_dimensions, 'angular')
        index.load(file_path)
        if index.get_n_items() > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error validating Annoy index file: {str(e)}")
        return False

def create_and_save_annoy_index(df, file_path='datasets/item_similarity.ann'):
    features, tfidf, scaler = create_feature_matrix(df)
    num_dimensions = features.shape[1]
    
    if not os.path.exists(file_path) or not is_valid_annoy_file(file_path, num_dimensions):
        print(f"Annoy index file '{file_path}' not found or invalid. Building a new one...")
        annoy_index = build_annoy_index(features)
        try:
                annoy_index.save(file_path)
                print(f"Annoy index saved successfully at {file_path}")
        except Exception as e:
                print(f"Error saving Annoy index: {str(e)}")
    else:
        print(f"Annoy index file '{file_path}' found and valid. Loading the existing index...")
        annoy_index = AnnoyIndex(num_dimensions, 'angular')
        annoy_index.load(file_path)
        print(f"Annoy index loaded successfully from {file_path}")
    
    return features, tfidf, scaler

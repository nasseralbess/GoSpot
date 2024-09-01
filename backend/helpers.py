from flask import current_app
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import random
from annoy import AnnoyIndex
from random import uniform

# from routes.user_routes import retrieve_user_preferences, update_user_preferences
def get_db():
    return current_app.config['db']

def get_features():
    return current_app.config['features']

def get_reverse_category_mapping():
    return current_app.config['reverse_category_mapping']

def get_tfidf():
    return current_app.config['tfidf']

def get_df():
    return current_app.config['df']

def get_coordinate_scaler():
    return current_app.config['coordinate_scaler']


def get_annoy_index():
    features = current_app.config['features']
    f = features.shape[1]  # Number of dimensions (features) in each vector

    # Initialize the Annoy index with the correct dimensionality and specify the use of angular distance.
    annoy_index = AnnoyIndex(f, 'angular')

    annoy_index.load(current_app.config['annoy_index_path'])

    return annoy_index

def get_user_profile(user_id, tfidf, coordinate_scaler):
    print("Yousef")
    db = get_db()
    user = db['User']
    features = get_features()
    reverse_category_mapping = get_reverse_category_mapping()
    df = get_df()

    if not list(user.find_one({'_id': user_id})):
        return np.zeros(features.shape[1])
    
    user_vector = np.zeros(features.shape[1])
    user_data = list(user.find({'_id': user_id}))[0]
    
    general_prefs = user_data['general_preferences']
    for category in general_prefs['categories']:
        
        mapped_category = reverse_category_mapping.get(category, 'other').lower()
        print('mapped_category:', mapped_category)
        print('vocab:', tfidf.vocabulary_) 
        if mapped_category in tfidf.vocabulary_:
            print('edited user vector')
            print('idx:',tfidf.vocabulary_[mapped_category])
            user_vector[tfidf.vocabulary_[mapped_category]] = 1
    print('vector:',sum(user_vector))
    

    price_index = features.shape[1] - 4 + len(general_prefs['price']) -1 
    user_vector[price_index] = 1
    
   

    for spot_id, spot_data in user_data['location_specific'].items():
        spot_index = df[df['id'] == spot_id].index
        if len(spot_index) > 0:
            spot_index = spot_index[0]
            
            if not spot_data.get('time_viewing', True):
                # User pressed details, incorporate positive interactions
                interaction_weight = 1.0
                
                if spot_data.get('pressed_share', False):
                    interaction_weight += 0.3
                if spot_data.get('pressed_save', False):
                    interaction_weight += 0.3
                
                # Incorporate viewing time
                max_viewing_time = 60
                viewing_time = min(spot_data.get('time_viewing', 0), max_viewing_time)
                time_factor = viewing_time / max_viewing_time
                interaction_weight *= (1 + time_factor)
                
                # Incorporate rating with penalty for low ratings
                rating = spot_data.get('rating', 2.5)
                if rating < 3:
                    # Apply penalty that increases as rating approaches 1
                    penalty = 1 - (rating - 1) / 2  # This will be 1 at rating 1, and 0 at rating 3
                    interaction_weight *= (1 - penalty * 0.5)  # Adjust the 0.5 to control penalty strength
                
                # Add to user vector
                user_vector += features[spot_index] * interaction_weight
            
            else:
                # User didn't press details, subtract a fraction of the feature vector
                user_vector -= features[spot_index] * 0.2

    norm = np.linalg.norm(user_vector)
    if norm > 0:
        user_vector /= norm


    return user_vector


def get_group_profile(user_ids):
    group_vector = np.zeros(get_features().shape[1])
    db = get_db()

    for user_id in user_ids:
        group_vector += db['UserVectors'].find_one({'_id': user_id})['vector']
    
    # Normalize the group vector
    norm = np.linalg.norm(group_vector)
    if norm > 0:
        group_vector /= norm
    
    return group_vector


def popular_items_recommend(n):
    # Recommend based on a combination of rating and review count
    df = get_df()
    scores = df['review_count'] * df['rating'].fillna(0)
    top_indices = scores.argsort()[-n:][::-1]
    recommended_ids = df.iloc[top_indices]['id'].tolist()
    return recommended_ids


def user_based_recommend(user_id, n, randomness_factor=0.5):
    """
    Recommend items to a user based on user similarity scores with added randomness.

    Parameters:
    - user_id: The ID of the user to whom we want to recommend items.
    - n: The number of items to recommend.
    - randomness_factor: The magnitude of the randomness added to the scores. 
      Default is 0.1. Increase this to add more randomness.

    Returns:
    - A list of recommended item IDs.
    """
    db = get_db()  # Get the database connection
    user = db['User']  # Reference to the 'User' collection
    features = get_features()  # Get the item feature matrix
    df = get_df()  # Get the DataFrame containing item details

    user_id = int(user_id)  # Ensure user_id is an integer

    # If user_id is not found in the database, return popular items
    if user_id not in user.distinct('_id'):
        return popular_items_recommend(n)
    
    # Retrieve the user's profile vector from the 'UserVectors' collection
    user_profile = db['UserVectors'].find_one({'_id': user_id})['vector']
    # Compute cosine similarity scores between the user's profile and item features
    scores = cosine_similarity([user_profile], features)[0]

    # Add randomness to the scores to introduce diversity in recommendations
    random_noise = np.random.uniform(-randomness_factor, randomness_factor, size=scores.shape)
    scores_with_randomness = scores + random_noise
    
    # Get the top n item indices based on the modified scores
    top_indices = scores_with_randomness.argsort()[-n:][::-1]
    
    # Retrieve the IDs of the recommended items
    recommended_ids = df.iloc[top_indices]['id'].tolist()
    
    return recommended_ids

def item_based_recommend(base_items, n):
    df = get_df()
    annoy_index = get_annoy_index()
    base_indices = df[df['id'].isin(base_items)].index

    similar_items = set()
    for idx in base_indices:
        similar_indices = annoy_index.get_nns_by_item(idx, n)
        similar_items.update(df.iloc[similar_indices]['id'].tolist())
    
    similar_items = list(similar_items - set(base_items))
    
    # If we don't have enough similar items, pad with popular items
    if len(similar_items) < n:
        popular = popular_items_recommend(n - len(similar_items))
        similar_items.extend(popular)
    return similar_items[:n]


def group_based_recommend(user_ids, n=10):
    features = get_features()
    df = get_df()
    group_profile = get_group_profile(user_ids)
    scores = cosine_similarity([group_profile], features)[0]
    
    top_indices = scores.argsort()[-n:][::-1]
    recommended_ids = df.iloc[top_indices]['id'].tolist()
    return recommended_ids

def least_misery_group_recommend(user_ids, n=10):
    individual_scores = []
    features = get_features()
    df = get_df()
    for user_id in user_ids:
        user_profile = get_db()['UserVectors'].find_one({'_id': user_id})['vector']
        scores = cosine_similarity([user_profile], features)[0]
        individual_scores.append(scores)
    
    # Take the minimum score for each item across all users
    group_scores = np.min(individual_scores, axis=0)
    
    top_indices = group_scores.argsort()[-n:][::-1]
    recommended_ids = df.iloc[top_indices]['id'].tolist()
    
    return recommended_ids

def get_group_recommendation(user_ids):
    # You could alternate between different group recommendation strategies
    strategies = [group_based_recommend, least_misery_group_recommend]
    strategy = random.choice(strategies)
    user_ids = [int(user_id) for user_id in user_ids]
    recommendations = strategy(user_ids, n=10)
    if recommendations:
        return recommendations
    else:
        return None
    
def get_next_items(user_id, n=10):
    # Ensure n is even
    n = n if n % 2 == 0 else n + 1
    
    # Get n/2 recommendations based on user profile
    user_based_recommendations = user_based_recommend(user_id, n // 2)
    
    # Get n/2 recommendations based on item similarity to the user-based recommendations
    item_based_recommendations = item_based_recommend(user_based_recommendations, n // 2)
    
    # Combine and shuffle the recommendations
    all_recommendations = user_based_recommendations + item_based_recommendations
    random.shuffle(all_recommendations)
    return all_recommendations

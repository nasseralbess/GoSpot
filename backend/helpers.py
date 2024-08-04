from flask import current_app
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import random

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

# def get_spot_details():
#     return current_app.config['spot_details']
# def get_item_similarity():
#     return current_app.config['item_similarity']

def get_user_profile(user_id, tfidf, coordinate_scaler):
    db = get_db()
    user = db['User']
    features = get_features()
    reverse_category_mapping = get_reverse_category_mapping()
    df = get_df()

    if not list(user.find_one({'_id': user_id})):
        return np.zeros(features.shape[1])
    
    user_vector = np.zeros(features.shape[1])
    user_data = list(user.find({'_id': user_id}))[0]
    # print('user data: ',user_data)
    general_prefs = user_data['general_preferences']
    for category in general_prefs['categories']:
        mapped_category = reverse_category_mapping.get(category, category)
        if mapped_category in tfidf.vocabulary_:
            user_vector[tfidf.vocabulary_[mapped_category]] = 1
    
    price_index = features.shape[1] - 4 + len(general_prefs['price'])
    user_vector[price_index] = 1
    
    user_coords = np.array(general_prefs['coordinates']).reshape(1, -1)
    # Create a dummy array with 4 features to match the scaler's expected input
    dummy_coords = np.zeros((1, 4))
    dummy_coords[0, 2:] = user_coords  # Assuming latitude and longitude are the last two features
    scaled_coords = coordinate_scaler.transform(dummy_coords)
    user_vector[-6:-4] = scaled_coords[0, 2:] 

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


def get_group_profile(user_ids, tfidf, coordinate_scaler):
    features = get_features()
    group_vector = np.zeros(features.shape[1])
    for user_id in user_ids:
        user_vector = get_user_profile(user_id, tfidf, coordinate_scaler)
        group_vector += user_vector
    
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


def user_based_recommend(user_id, n):
    db = get_db()
    user = db['User']
    features = get_features()
    df = get_df()
    tfidf = get_tfidf()
    # spot_details = get_spot_details()
    coordinate_scaler = get_coordinate_scaler()
    if user_id not in user.distinct('_id'):
        # New user: use a fallback method (e.g., popular items)
        return popular_items_recommend(n)
    
    user_profile = get_user_profile(user_id, tfidf, coordinate_scaler)
    scores = cosine_similarity([user_profile], features)[0]
    
    top_indices = scores.argsort()[-n:][::-1]
    recommended_ids = df.iloc[top_indices]['id'].tolist()
    
    return recommended_ids


# def item_based_recommend(base_items, n):
#     df = get_df()
#     item_similarity = get_item_similarity()
#     spot_details = get_spot_details()
#     base_indices = df[df['id'].isin(base_items['id'])].index
    
#     similar_items = set()
#     for idx in base_indices:
#         # Get top similar items for each base item
#         similar_indices = item_similarity[idx].argsort()[-n:][::-1]
#         similar_items.update(df.iloc[similar_indices]['id'].tolist())
    
#     # Remove base items from similar items
#     similar_items = list(similar_items - set(base_items['id']))
    
#     # If we don't have enough similar items, pad with popular items
#     if len(similar_items) < n:
#         popular = popular_items_recommend(n - len(similar_items))
#         similar_items.extend(popular['id'].tolist())
    
#     return spot_details[spot_details['id'].isin(similar_items[:n])][['id', 'name', 'image_url', 'phone']]

def group_based_recommend(user_ids, n=10):
    features = get_features()
    df = get_df()
    tfidf = get_tfidf()
    # spot_details = get_spot_details()
    coordinate_scaler = get_coordinate_scaler()
    group_profile = get_group_profile(user_ids, tfidf, coordinate_scaler)
    scores = cosine_similarity([group_profile], features)[0]
    
    top_indices = scores.argsort()[-n:][::-1]
    recommended_ids = df.iloc[top_indices]['id'].tolist()
    return recommended_ids
    # return spot_details[spot_details['id'].isin(recommended_ids)][['id', 'name', 'image_url', 'phone']]

def least_misery_group_recommend(user_ids, n=10):
    individual_scores = []
    features = get_features()
    df = get_df()
    tfidf = get_tfidf()
    # spot_details = get_spot_details()
    coordinate_scaler = get_coordinate_scaler()
    for user_id in user_ids:
        user_profile = get_user_profile(user_id, tfidf, coordinate_scaler)
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
    
    recommendations = strategy(user_ids, n=10)
    if not recommendations.empty:
        return recommendations.iloc[0]
    else:
        return None
    
def get_next_items(user_id, n=10):
    # Ensure n is even
    n = n if n % 2 == 0 else n + 1
    
    # Get n/2 recommendations based on user profile
    user_based_recommendations = user_based_recommend(user_id, n)#n // 2)
    
    # Get n/2 recommendations based on item similarity to the user-based recommendations
    #item_based_recommendations = item_based_recommend(user_based_recommendations, n // 2)
    
    # Combine and shuffle the recommendations
    #all_recommendations = pd.concat([user_based_recommendations, item_based_recommendations])
    # all_recommendations.sample(n=len(all_recommendations))
    # return all_recommendations
    return user_based_recommendations


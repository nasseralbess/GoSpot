# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.3
#   kernelspec:
#     display_name: 'Python 3.11.0 (''venv'': venv)'
#     language: python
#     name: python3
# ---

import pandas as pd, json, numpy as np, random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime


# +
spots = json.load(open('Updating_datasets/data.json'))

spots = spots['businesses']

spots[0]
#keys to be kept in the recommendation system dataset:
#id, categories, review_count, rating, price, coordinates
#The rest of the keys are to be stored in a separate dataset for the user's knowledge
#keep id in both datasets to link them together
initial_weights = []
spot_details = []
for spot in spots:
    rec={}
    use={}
    for key in spot:
        if key == 'id':
            rec[key]=spot[key]
            use[key]=spot[key]
        else:
            if key in ['categories','review_count','rating','price','coordinates']:
                rec[key]=spot[key]
            else:
                use[key]=spot[key]
        
    initial_weights.append(rec)
    spot_details.append(use)

#Adding keys with made up random values to test drive integrating features into the recommender system.
#New Keys: 
# time_viewing [How much time the user spent looking at the place] (float)
# pressed_details [If the user pressed the details button] (bool)
# pressed_share [If they pressed share button] (bool)
# pressed_save [If they saved the place] (bool)

#user_preferences will be a two layer nesteddictionary with the user id as the key and a dictionary of the user's preferences as the value, 
# the user preferences is a nested dict where keys are spot ids, and values are spot specific preferences below is a sample of what the 
#user_preferences dictionary will look like
# The id will look something like this fk2hLMdVgDs8FKqwt_Q1ug
# The user id will look something like this 668653d1b87343725d7bb45f
user_preferences = {
    1:{#uid
        'location_specific':{
            28384:{#spot_id
                'time_viewing':5.0,'pressed_details':True,'pressed_share':False,'pressed_save':True,
                'rating':5.0
            },
            28384:{#spot_id
                'swiped_left':False,'swiped_right':True,'time_viewing':3.0,'pressed_details':True,'pressed_share':False,'pressed_save':True,
                'rating':4.0
            },
        },
        'general_preferences':{
            'price':'$$',
            'categories':['restaurant','bar'],
            'coordinates':(39.9526,75.1652)
        }
    }
}
# print("Spot Details:")
# display(spot_details[0])
# print("Initial Weights:")
# display(initial_weights[0])
# print("User Preferences:")
# display(user_preferences)

#unique categories
# categories = set()
# for spot in initial_weights:
#     for category in spot['categories']:
#         for key,value in category.items():
#             if key == 'title':
#                 categories.add(value)
# list(categories)
# initial_weights[0]
# temp={}
# for entry in initial_weights:
#     temp[entry['id']]=entry
#     del temp[entry['id']]['id']
# initial_weights=temp
# temp={}
# for entry in spot_details:
#     temp[entry['id']]=entry
#     del temp[entry['id']]['id']
# spot_details=temp
# json.dump(initial_weights,open('Updating_datasets/initial_weights.json','w'))
# json.dump(spot_details,open('Updating_datasets/spot_details.json','w'))

# +
# Required for recommendation method get_next_items and get_group
category_mapping = {
    'American': ['American', 'New American', 'Southern', 'Soul Food', 'Cajun/Creole', 'Tex-Mex'],
    'Asian': ['Chinese', 'Japanese', 'Korean', 'Thai', 'Vietnamese', 'Indian', 'Pakistani', 'Bangladeshi', 'Taiwanese', 'Filipino', 'Malaysian', 'Indonesian', 'Singaporean', 'Burmese', 'Cambodian', 'Laotian', 'Mongolian', 'Nepalese', 'Sri Lankan', 'Asian Fusion'],
    'European': ['Italian', 'French', 'Spanish', 'German', 'Greek', 'British', 'Irish', 'Scottish', 'Polish', 'Russian', 'Ukrainian', 'Hungarian', 'Czech', 'Austrian', 'Belgian', 'Dutch', 'Swiss', 'Scandinavian', 'Portuguese'],
    'Latin American': ['Mexican', 'Brazilian', 'Peruvian', 'Argentine', 'Colombian', 'Venezuelan', 'Cuban', 'Puerto Rican', 'Dominican', 'Salvadoran', 'Honduran', 'Nicaraguan', 'Guatemalan', 'Ecuadorian', 'Bolivian', 'Chilean'],
    'Middle Eastern': ['Lebanese', 'Turkish', 'Persian/Iranian', 'Israeli', 'Moroccan', 'Egyptian', 'Syrian', 'Armenian', 'Afghan', 'Iraqi', 'Uzbek', 'Georgian'],
    'African': ['Ethiopian', 'Nigerian', 'Ghanaian', 'Senegalese', 'South African', 'Eritrean', 'Somali', 'Kenyan', 'Tanzanian', 'Ugandan'],
    'Seafood': ['Seafood', 'Sushi Bars', 'Fish & Chips', 'Poke'],
    'Fast Food': ['Fast Food', 'Burgers', 'Pizza', 'Sandwiches', 'Hot Dogs', 'Chicken Wings'],
    'Vegetarian and Vegan': ['Vegetarian', 'Vegan', 'Raw Food'],
    'Breakfast and Brunch': ['Breakfast & Brunch', 'Pancakes', 'Waffles', 'Bagels', 'Donuts'],
    'Bakeries and Desserts': ['Bakeries', 'Desserts', 'Ice Cream & Frozen Yogurt', 'Cupcakes', 'Patisserie/Cake Shop', 'Gelato'],
    'Cafes and Coffee Shops': ['Cafes', 'Coffee & Tea', 'Bubble Tea'],
    'Bars and Pubs': ['Bars', 'Pubs', 'Sports Bars', 'Wine Bars', 'Beer Gardens', 'Cocktail Bars', 'Dive Bars', 'Hookah Bars'],
    'Specialty Food': ['Cheese Shops', 'Butcher', 'Farmers Market', 'Specialty Food', 'Organic Stores', 'Health Markets'],
    'Food Trucks and Stands': ['Food Trucks', 'Food Stands', 'Street Vendors'],
    'Grocery': ['Grocery', 'International Grocery', 'Convenience Stores'],
    'Nightlife': ['Nightlife', 'Dance Clubs', 'Karaoke', 'Comedy Clubs', 'Jazz & Blues'],
    'Arts and Entertainment': ['Museums', 'Art Galleries', 'Performing Arts', 'Music Venues', 'Theaters', 'Cinema'],
    'Outdoor Activities': ['Parks', 'Beaches', 'Hiking', 'Botanical Gardens', 'Playgrounds', 'Dog Parks'],
    'Fitness and Sports': ['Gyms', 'Yoga', 'Martial Arts', 'Swimming Pools', 'Tennis', 'Basketball Courts', 'Soccer'],
    'Shopping': ['Shopping Centers', 'Clothing', 'Shoes', 'Jewelry', 'Books', 'Electronics', 'Home & Garden'],
    'Beauty and Spas': ['Hair Salons', 'Nail Salons', 'Day Spas', 'Massage'],
    'Hotels and Accommodation': ['Hotels', 'Hostels', 'Bed & Breakfast'],
    'Event Planning and Services': ['Wedding Planning', 'Party & Event Planning', 'Caterers', 'Photographers'],
    'Automotive': ['Car Dealers', 'Auto Repair', 'Car Wash', 'Gas Stations'],
    'Professional Services': ['Lawyers', 'Accountants', 'Real Estate', 'Insurance'],
    'Education': ['Schools', 'Colleges', 'Tutoring', 'Cooking Classes', 'Art Schools'],
    'Pets': ['Pet Stores', 'Veterinarians', 'Pet Groomers', 'Dog Walkers'],
    'Religious Organizations': ['Churches', 'Mosques', 'Synagogues', 'Temples'],
    'Other': []  # Catch-all for categories that don't fit elsewhere
}

# Create a reverse mapping for easy lookup
reverse_category_mapping = {sub_cat: main_cat for main_cat, sub_cats in category_mapping.items() for sub_cat in sub_cats}


# Load the data
with open('Updating_datasets/initial_weights.json', 'r') as file:
    data = json.load(file)

index=[]
vals = []
for key,value in data.items():
    index.append(key)
    vals.append([val for val in value.values()])
    
initial_weights = pd.DataFrame(vals,columns=[key for key in data[index[0]].keys()],index=index)

with open('Updating_datasets/spot_details.json', 'r') as file:
    spot_details = json.load(file)
index,vals = [],[]
# print(spot_details)
for key,value in spot_details.items():
    index.append(key)
    vals.append([val for val in value.values()])
# print(len(vals),len(index))

spot_details = pd.DataFrame(vals,columns=[key for key in spot_details[index[0]].keys()],index=index)
spot_details = spot_details.copy().reset_index()
spot_details.rename(columns={'index': 'id'}, inplace=True)
user_preferences = {}

def preprocess_data(initial_weights):
    df = initial_weights.copy().reset_index()
    df.rename(columns={'index': 'id'}, inplace=True)
    
    # Extract categories and map to general categories
    df['categories'] = df['categories'].apply(lambda x: [reverse_category_mapping.get(cat['title'], 'Other') for cat in x])
    df['categories'] = df['categories'].apply(lambda x: ', '.join(set(x)) if x else 'Other')
    
    # Handle missing values
    df['review_count'] = df['review_count'].fillna(0)
    df['rating'] = df['rating'].fillna(0)
    df['price'] = df['price'].fillna('$')
    df['latitude'] = df['coordinates'].apply(lambda x: x['latitude'] if x and 'latitude' in x else 0)
    df['longitude'] = df['coordinates'].apply(lambda x: x['longitude'] if x and 'longitude' in x else 0)
    df = df.drop(columns=['coordinates'])
    
    return df



df = preprocess_data(initial_weights)
print(df)


# +
# Required for recommendation method get_next_items and get_group
def create_feature_matrix(df):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['categories'])
    
    scaler = MinMaxScaler()
    numerical_features = scaler.fit_transform(df[['review_count', 'rating', 'latitude', 'longitude']].fillna(0))
    
    price_dummies = pd.get_dummies(df['price'], prefix='price').fillna(0)
    
    features = np.hstack((tfidf_matrix.toarray(), numerical_features, price_dummies.values))
    
    return features, tfidf, scaler

features, tfidf, coordinate_scaler = create_feature_matrix(df)
item_similarity = cosine_similarity(features)


# +
# Function to get user profile
def get_user_profile(user_id, tfidf, coordinate_scaler):
    if user_id not in user_preferences:
        return np.zeros(features.shape[1])
    
    user_vector = np.zeros(features.shape[1])
    user_data = user_preferences[user_id]
    
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
            
            if spot_data.get('pressed_details', False):
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



# Convert 
def add_new_user(user_id, general_preferences):
    if user_id in user_preferences:
        raise ValueError("User ID already exists")
    
    user_preferences[user_id] = {
        'general_preferences': general_preferences,
        'location_specific': {},
        'last_active': datetime.now()
    }
    print(f"New user {user_id} added successfully")
# Convert 
def update_user_preferences(user_id, new_preferences):
    if user_id not in user_preferences:
        raise ValueError("User ID does not exist")
    
    user_preferences[user_id]['general_preferences'].update(new_preferences)
    user_preferences[user_id]['last_active'] = datetime.now()
    print(f"Preferences updated for user {user_id}")
# Convert 
def record_spot_interaction(user_id, spot_id, interaction):
    if user_id not in user_preferences:
        raise ValueError("User ID does not exist")
    
    if spot_id not in user_preferences[user_id]['location_specific']:
        user_preferences[user_id]['location_specific'][spot_id] = {}
    
    user_preferences[user_id]['location_specific'][spot_id].update(interaction)
    user_preferences[user_id]['last_active'] = datetime.now()
    print(f"Interaction recorded for user {user_id} with spot {spot_id}")

# def get_user_stats(user_id):
#     if user_id not in user_preferences:
#         raise ValueError("User ID does not exist")
    
#     user_data = user_preferences[user_id]
#     total_interactions = len(user_data['location_specific'])
#     likes = sum(1 for spot in user_data['location_specific'].values() if spot.get('pressed_details', False))
    
#     return {
#         'total_interactions': total_interactions,
#         'likes': likes,
#         'last_active': user_data['last_active']
#     }

# Convert 
def update_user_coordinates(user_id, new_coordinates):
    if user_id not in user_preferences:
        raise ValueError("User ID does not exist")
    
    user_preferences[user_id]['general_preferences']['coordinates'] = new_coordinates
    user_preferences[user_id]['last_active'] = datetime.now()
    print(f"Coordinates updated for user {user_id}")

import random

    
def get_next_items(user_id, n=10):
    # Ensure n is even
    n = n if n % 2 == 0 else n + 1
    
    # Get n/2 recommendations based on user profile
    user_based_recommendations = user_based_recommend(user_id, n // 2)
    
    # Get n/2 recommendations based on item similarity to the user-based recommendations
    item_based_recommendations = item_based_recommend(user_based_recommendations, n // 2)
    
    # Combine and shuffle the recommendations
    all_recommendations = pd.concat([user_based_recommendations, item_based_recommendations])
    all_recommendations.sample(n=len(all_recommendations))
    return all_recommendations
    
def user_based_recommend(user_id, n):
    if user_id not in user_preferences:
        # New user: use a fallback method (e.g., popular items)
        return popular_items_recommend(n)
    
    user_profile = get_user_profile(user_id, tfidf, coordinate_scaler)
    scores = cosine_similarity([user_profile], features)[0]
    
    top_indices = scores.argsort()[-n:][::-1]
    recommended_ids = df.iloc[top_indices]['id'].tolist()
    
    return spot_details[spot_details['id'].isin(recommended_ids)][['id', 'name', 'image_url', 'phone']]

def item_based_recommend(base_items, n):
    base_indices = df[df['id'].isin(base_items['id'])].index
    
    similar_items = set()
    for idx in base_indices:
        # Get top similar items for each base item
        similar_indices = item_similarity[idx].argsort()[-n:][::-1]
        similar_items.update(df.iloc[similar_indices]['id'].tolist())
    
    # Remove base items from similar items
    similar_items = list(similar_items - set(base_items['id']))
    
    # If we don't have enough similar items, pad with popular items
    if len(similar_items) < n:
        popular = popular_items_recommend(n - len(similar_items))
        similar_items.extend(popular['id'].tolist())
    
    return spot_details[spot_details['id'].isin(similar_items[:n])][['id', 'name', 'image_url', 'phone']]

def popular_items_recommend(n):
    # Recommend based on a combination of rating and review count
    scores = df['review_count'] * df['rating'].fillna(0)
    top_indices = scores.argsort()[-n:][::-1]
    recommended_ids = df.iloc[top_indices]['id'].tolist()
    return spot_details[spot_details['id'].isin(recommended_ids)][['id', 'name', 'image_url', 'phone']]

# Update the get_next_spot function to use get_next_items
def get_next_spot(user_id):
    recommendations = get_next_items(user_id, n=10)  # Get 10 recommendations
    seen_spots = set(user_preferences[user_id]['location_specific'].keys())
    
    for _, spot in recommendations.iterrows():
        if spot['id'] not in seen_spots:
            return spot
    
    return None  # Return None if all recommended spots have been seen
def get_group_profile(user_ids, tfidf, coordinate_scaler):
    group_vector = np.zeros(features.shape[1])
    for user_id in user_ids:
        user_vector = get_user_profile(user_id, tfidf, coordinate_scaler)
        group_vector += user_vector
    
    # Normalize the group vector
    norm = np.linalg.norm(group_vector)
    if norm > 0:
        group_vector /= norm
    
    return group_vector
def group_based_recommend(user_ids, n=10):
    group_profile = get_group_profile(user_ids, tfidf, coordinate_scaler)
    scores = cosine_similarity([group_profile], features)[0]
    
    top_indices = scores.argsort()[-n:][::-1]
    recommended_ids = df.iloc[top_indices]['id'].tolist()
    
    return spot_details[spot_details['id'].isin(recommended_ids)][['id', 'name', 'image_url', 'phone']]
def get_next_group_spot(user_ids):
    recommendations = group_based_recommend(user_ids, n=20)  # Get more recommendations for groups
    
    # Get all seen spots for the group
    seen_spots = set()
    for user_id in user_ids:
        seen_spots.update(user_preferences[user_id]['location_specific'].keys())
    
    for _, spot in recommendations.iterrows():
        if spot['id'] not in seen_spots:
            return spot
    
def least_misery_group_recommend(user_ids, n=10):
    individual_scores = []
    for user_id in user_ids:
        user_profile = get_user_profile(user_id, tfidf, coordinate_scaler)
        scores = cosine_similarity([user_profile], features)[0]
        individual_scores.append(scores)
    
    # Take the minimum score for each item across all users
    group_scores = np.min(individual_scores, axis=0)
    
    top_indices = group_scores.argsort()[-n:][::-1]
    recommended_ids = df.iloc[top_indices]['id'].tolist()
    
    return spot_details[spot_details['id'].isin(recommended_ids)][['id', 'name', 'image_url', 'phone']]

    return None  # Return None if all recommended spots have been seen
def get_group_recommendation(user_ids):
    # You could alternate between different group recommendation strategies
    strategies = [group_based_recommend, least_misery_group_recommend]
    strategy = random.choice(strategies)
    
    recommendations = strategy(user_ids, n=1)
    if not recommendations.empty:
        return recommendations.iloc[0]
    else:
        return None

        
# def main():
#     # Adding a new user
#     add_new_user(1, {'price': '$$', 'categories': ['Italian', 'Bars'], 'coordinates': (39.9526, 75.1652)})
#     # User preference 
#     update_user_preferences(1, {'categories': ['Italian', 'Bars', 'Seafood']})
#     # Swiping activity
#     record_spot_interaction(1, 'j1S3NUrkB3BVT49n_e76NQ', {'pressed_details': None, 'time_viewing': 5.0})
#     record_spot_interaction(1, 'zj8Lq1T8KIC5zwFief15jg', {'time_viewing': 2.0})

#     next_spot = get_next_spot(1)
#     print("Next spot to show:", next_spot)

#     # stats = get_user_stats(1)
#     print("User stats:", stats)

    

if __name__ == "__main__":
    main()
# -



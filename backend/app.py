from pymongo import MongoClient
from flask_cors import CORS
from routes.user_routes import normal_route
# from helpers import *
from flask import Flask, request, jsonify
import json
from pymongo import MongoClient
from flask_cors import CORS
from routes.user_routes import normal_route
import hashlib
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
# ONLY FOR TESTING PURPOSES 
# from flask_wtf.csrf import CSRFProtect
from scipy.sparse import csr_matrix

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

# with open('Updating_datasets/spot_details.json', 'r') as file:
#     spot_details = json.load(file)
# index,vals = [],[]
# # print(spot_details)
# for key,value in spot_details.items():
#     index.append(key)
#     vals.append([val for val in value.values()])
# print(len(vals),len(index))

# spot_details = pd.DataFrame(vals,columns=[key for key in spot_details[index[0]].keys()],index=index)
# spot_details = spot_details.copy().reset_index()
# spot_details.rename(columns={'index': 'id'}, inplace=True)
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
#print(df)

#one time thing, should be saved into the database as read only, unless we expand with more datasets
def create_feature_matrix(df):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(df['categories'])
    
    scaler = MinMaxScaler()
    numerical_features = scaler.fit_transform(df[['review_count', 'rating', 'latitude', 'longitude']].fillna(0))
    
    price_dummies = pd.get_dummies(df['price'], prefix='price').fillna(0)
    
    features = np.hstack((tfidf_matrix.toarray(), numerical_features, price_dummies.values))
    
    return features, tfidf, scaler




def create_app():
    app = Flask(__name__)
    CORS(app)

    # MongoDB Atlas connection string
    client = MongoClient('mongodb+srv://loko:melike2004@lovelores.h1nkog2.mongodb.net/?retryWrites=true&w=majority&appName=LoveLores')
    db = client.GoSpot

    # Load and preprocess data
    df = preprocess_data(initial_weights)
    features, tfidf, coordinate_scaler = create_feature_matrix(df)
    # features_sparse = csr_matrix(features)
    # item_similarity = cosine_similarity(features_sparse, dense_output=False)
    #item_similarity = cosine_similarity(features)

    #app.config['item_similarity'] = item_similarity
    app.config['df'] = df
    app.config['tfidf'] = tfidf
    app.config['coordinate_scaler'] = coordinate_scaler
    app.config['features'] = features
    app.config['reverse_category_mapping'] = reverse_category_mapping
    app.config['db'] = db
    # app.config['spot_details'] = spot_details
    #app.config['item_similarity'] = item_similarity

    app.register_blueprint(normal_route, url_prefix='/user')

    return app

if __name__ == '__main__':
    app = create_app()
    
    # with app.app_context():
    #     from helpers import get_user_profile, get_tfidf, get_coordinate_scaler
    #     print(get_user_profile(1, get_tfidf(), get_coordinate_scaler()))
    
    app.run(debug=True)
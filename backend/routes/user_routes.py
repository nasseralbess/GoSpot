from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime
from helpers import *
from schemas.user_schema import UserInteractionSchema, UserSchema, UpdatePreferencesSchema

# Initialistion 
normal_route = Blueprint('normal_routes', __name__)

# User Schemas 
user_interaction_schema = UserInteractionSchema()
adding_user_schema = UserSchema()
updating_preferences = UpdatePreferencesSchema()



# Adds a user, and fail if user already exists
@normal_route.route('/add_user', methods=['POST'])
def add_new_user():
    data = request.json

    errors = adding_user_schema.validate(data)
    
    if errors:
        return jsonify(errors), 400


    db = current_app.config['db']

    user = db['User']

    # User generated from logto's 
    user_id = data.get('user_id')
    if user.find_one({'_id': user_id}):
        return jsonify({'error': 'User ID already exists'}), 400

    new_user = {
        '_id': user_id,
        'general_preferences': data.get('general_preferences'),
        'location_specific': {},
        'groups': [],
        'name': data.get('name'),
        'password': data.get('password'),
        'age': data.get('age'),
        'last_active': datetime.now()
    }

    user.insert_one(new_user)
    user_vector = get_user_profile(user_id, get_tfidf(), get_coordinate_scaler())
    vector_db = db['UserVector']
    vector_db.insert_one({
        '_id': user_id,
        'vector': user_vector.tolist()
    })
    return jsonify({'message': f"New user {user_id} added successfully"}), 201


# Updates the entire preferences
@normal_route.route('/update_preferences', methods=['PUT'])
def update_user_preferences():
    data = request.json
    print(f'\n\ndata: {data}\n\n')
    errors = updating_preferences.validate(data)

    if errors:
        return jsonify(errors), 400

    user_id = data.get('user_id')
    new_preferences = data.get('new_preferences')

    db = get_db()
    user = db['User']

    result = user.update_one(
        {'_id': user_id},
        {
            '$set': {
                'general_preferences': new_preferences,
                'last_active': datetime.now()
            }
        }
    )
    vector_db = db['UserVectors']
    user_vector = get_user_profile(user_id, get_tfidf(), get_coordinate_scaler())
   

    vector_db.update_one(
        {'_id': user_id},
        {
            '$set': {
                'vector': user_vector.tolist()
            }
        }
    )
    if result.modified_count:
        return jsonify({'message': f"Preferences updated for user {user_id}"}), 200
    else:
        return jsonify({'error': 'User not found or no changes made'}), 404


    
# Recording interactions of places for users 

@normal_route.route('/record_interaction', methods=['POST']) #save inside group 
def record_spot_interaction():
    data = request.json

    # Data validation
    errors = user_interaction_schema.validate(data)
    if errors:
        return jsonify({
            "message": "Data Structure Invalid, please ensure data structure is correct",
            "errors": (errors)
        }), 400
    
    user_id = data.get('user_id')
    # spot_id = data.get('spot_id')
    interactions = data.get('interaction')
    
    db = get_db()
    user = db['User']

    update_data = {
        '$set': {
            'last_active': datetime.now()
        }
    }

    for spot_id, interaction in interactions.items():
        update_data['$set'][f'location_specific.{spot_id}'] = interaction

    result = user.update_one(
        {'_id': user_id},
        update_data
    )

    if result.modified_count:
        return jsonify({'message': f"Interaction recorded for user {user_id} with spot {spot_id}"}), 200
    else:
        return jsonify({'error': 'User not found or no changes made'}), 404

# Updating coordinates 
# This could be redundant, as you can update coordinates in the update preferences
@normal_route.route('/update_coordinates', methods=['PUT'])
def update_user_coordinates():
    data = request.json
    user_id = data.get('user_id')
    new_coordinates = data.get('new_coordinates')

    db = get_db()
    user = db['User']

    result = user.update_one(
        {'_id': user_id},
        {
            '$set': {
                'general_preferences.coordinates': new_coordinates,
                'last_active': datetime.now()
            }
        }
    )
    if result.modified_count:
        return jsonify({'message': f"Coordinates updated for user {user_id}"}), 200
    else:
        return jsonify({'error': 'User not found or no changes made'}), 404


# Not working for string ids 
# Specifiy the amount of items to get with maximum
@normal_route.route('/get_next_spot', methods=['GET'])
def get_next_spot():
    user_id = request.args.get('user_id')
    num_items = request.args.get('num_items', default=1, type=int)  # New query parameter to specify the number of items
    
    next_spot = get_next_items(user_id)
    db = get_db()
    user = db['User']
    
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'message': 'Invalid user_id'}), 400
   
    ret = set()  # Use a set to ensure unique items
    seen = list(user.find_one({'_id': user_id}).get('location_specific', {}).keys())
    
    if not next_spot:
        return jsonify({'message': 'No more spots available'}), 404
    
    for id in next_spot:
        if id not in seen:
            ret.add(id)
        if len(ret) >= num_items:  # Stop when the desired number of items is reached
            break
    
    if ret:
        return jsonify(list(ret)), 200
    
    return jsonify({'message': 'No more spots available'}), 404

@normal_route.route('/retrieve_current_preferences', methods=['GET'])
def retrieve_user_preferences():
    user_id = request.args.get('user_id')
    db = get_db()
    user_collection = db['User']
    
    # Query the user document by user_id
    user = user_collection.find_one({"_id": int(user_id)})
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Assuming 'general_preferences' is the field containing the user's preferences
    preferences = user.get('general_preferences', {})
    
    return jsonify(preferences), 200


# Create the route
@normal_route.route('/retrieve_details', methods=['POST'])
def retrieve_details():
    
    data = request.json
    # Extract the list of spot IDs
    spotLists = data['spotLists']

    # Connect to the database
    db = get_db()
    spots = db['Spot']

    # Query to find documents with the specified IDs
    query = {"_id": {"$in": spotLists}}
    results = list(spots.find(query))

    # Optionally, you could serialize the results using Marshmallow
    return jsonify(results), 200


@normal_route.route('/clear_spot_data', methods=['GET'])
def clear_spot_data():
    """
    Clear spot data for a specific user while archiving the existing spot data.
    """
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    user_id = int(user_id)  # Ensure user_id is an integer
    db = get_db()
    user_collection = db['User']
    archive_collection = db['archived_locations']
    
    try:
        # Start a transaction to ensure atomicity
        with db.client.start_session() as session:
            with session.start_transaction():
                user = user_collection.find_one({'_id': user_id}, session=session)
                if not user:
                    return jsonify({'error': 'User not found'}), 404
                
                # Archive each location-specific place separately
                location_specific = user.get('location_specific', {})
                for place_id, details in location_specific.items():
                    archive_doc = {
                        'user_id': user_id,
                        'place_id': place_id,
                        'details': details,
                        'archived_time': datetime.now()
                    }
                    archive_collection.insert_one(archive_doc, session=session)
                
                # Clear the location-specific data
                result = user_collection.update_one(
                    {'_id': user_id},
                    {'$set': {'location_specific': {}}},
                    session=session
                )
                
                if result.modified_count:
                    return jsonify({'message': f"Spot data cleared for user {user_id}"}), 200
                else:
                    return jsonify({'error': 'No changes made'}), 404

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500


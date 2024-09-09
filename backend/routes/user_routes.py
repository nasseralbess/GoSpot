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



# 
# 
# Saved spots 
# 
@normal_route.route('/retrieve_all_saved', methods=['GET'])
def retrieve_all_saved():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    user_id = int(user_id)  # Convert user_id to integer
    db = get_db()
    users_db = db['User']
    archive_db = db['archived_locations']

    # Query to find the document for the specified user ID in the User collection
    user_data = users_db.find_one({'_id': user_id})
    if not user_data:
        return jsonify({"error": "User not found"}), 404

    # Extract the location_specific field (assumed to be an object)
    location_specific = user_data.get('location_specific', {})
    saved_places = [
        place_id
        for place_id, place_data in location_specific.items()
        if place_data.get('pressed_save') == "True"
    ]

    # Query the ArchivedLocations collection for saved places
    archived_places = list(archive_db.find({
        'user_id': user_id,
        'details.pressed_save': "True"
    }, {
        '_id': 0, 'place_id': 1  # Project only place_id, exclude _id from result
    }))

    # Combine saved places from both active and archived locations (only place_id)
    saved_places.extend(place['place_id'] for place in archived_places)

    return jsonify(saved_places), 200

# Create collection category 
@normal_route.route('/create_collection', methods=['POST'])
def create_collection():
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name')
    description = data.get('description', '')

    if not user_id or not name:
        return jsonify({'error': 'User ID and Collection Name are required'}), 400

    db = get_db()
    collections_db = db['categories']

    # Create the new collection
    new_collection = {
        "user_id": user_id,
        "name": name,
        "description": description,
        "places": [],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = collections_db.insert_one(new_collection)

    return jsonify({"message": "Collection created", "collection_id": str(result.inserted_id)}), 201

# Added places into category 
@normal_route.route('/add_to_collection', methods=['PUT'])
def add_to_collection():
    data = request.json
    collection_id = data.get('collection_id')
    place_id = data.get('place_id')

    if not collection_id or not place_id:
        return jsonify({'error': 'Collection ID and Place ID are required'}), 400

    db = get_db()
    collections_db = db['categories']

    # Find and update the collection by adding the place_id
    result = collections_db.update_one(
        {"_id": ObjectId(collection_id)},
        {"$addToSet": {"places": place_id}, "$set": {"updated_at": datetime.utcnow()}}
    )

    if result.matched_count == 0:
        return jsonify({'error': 'categories not found'}), 404

    return jsonify({"message": "Place added to categories"}), 200


# Retrieving all category
@normal_route.route('/retrieve_categories', methods=['GET'])
def retrieve_categories():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    db = get_db()
    collections_db = db['categories']

    # Query to retrieve all categories for the user
    categories = list(collections_db.find(
        {"user_id": int(user_id)},
        {"_id": 1, "name": 1, "description": 1, "places": 1}
    ))

    # Format the response
    formatted_categories = [
        {
            "category_id": str(category['_id']),
            "name": category.get('name'),
            "description": category.get('description', ''),
            "places": category.get('places', [])
        }
        for category in categories
    ]

    return jsonify(formatted_categories), 200

# Removing a place from a category 
@normal_route.route('/remove_from_collection', methods=['PUT'])
def remove_from_collection():
    data = request.json
    collection_id = data.get('collection_id')
    place_id = data.get('place_id')

    if not collection_id or not place_id:
        return jsonify({'error': 'Collection ID and Place ID are required'}), 400

    db = get_db()
    collections_db = db['categories']

    # Find and update the collection by removing the place_id
    result = collections_db.update_one(
        {"_id": ObjectId(collection_id)},
        {"$pull": {"places": place_id}, "$set": {"updated_at": datetime.utcnow()}}
    )

    if result.matched_count == 0:
        return jsonify({'error': 'Collection not found'}), 404

    return jsonify({"message": "Place removed from collection"}), 200

# NEED TO RUN AUTHENTICATION FOR THIS
# Deleting an entire category 
@normal_route.route('/delete_category', methods=['DELETE'])
def delete_category():
    category_id = request.args.get('category_id')

    if not category_id:
        return jsonify({'error': 'Category ID is required'}), 400

    db = get_db()
    collections_db = db['categories']

    # Delete the category by category_id
    result = collections_db.delete_one({"_id": ObjectId(category_id)})

    if result.deleted_count == 0:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify({"message": "Category deleted successfully"}), 200









# When you clear, you only clear the location_specific for the algorithm to restart
# But you archive those locations, and can still see them in your saved
# This is all so that we can perserve it for analytics later on 
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


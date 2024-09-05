from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime
from helpers import *
from schemas.user_schema import UserInteractionSchema, UserSchema, UpdatePreferencesSchema

# Initialistion 
normal_route = Blueprint('normal_routes', __name__)

# Schemas 
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
@normal_route.route('/record_interaction', methods=['POST'])
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
#Group Section
#
@normal_route.route('/get_group_spot', methods=['GET'])
def get_next_group_spot():
    group_id = request.args.get('group_id')
    groups_collection = get_db()['Groups']
    try:
        group = groups_collection.find_one({'_id': group_id})
        if group is None:
            return jsonify({'error': 'Group not found'}), 404

        user_ids = group.get('members', [])
        
        group_spot = get_group_recommendation(user_ids)
    

        if group_spot is not None:
            return jsonify(group_spot), 200
        else:
            return jsonify({'message': 'No group spot available'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@normal_route.route('/create_group', methods=['POST'])
def create_group():
    data = request.json
    group_id = data.get('group_id')
    group_name = data.get('group_name')
    groups = get_db()['Groups']
    groups.insert_one({
        '_id': group_id,
        'members': [data.get('creator')],
        'group_name': group_name
    })
    return jsonify({'group created': group_id}), 200



@normal_route.route('/add_to_group', methods=['POST'])
def add_to_group():
    data = request.json
    group_id = data.get('group_id')
    user_id = data.get('user_id')
    groups = current_app.config['db']['Groups']
    groups.update_one(
        {'_id': group_id},
        {
            '$addToSet': {
                'members': user_id
            }
        }
    )
    return jsonify({'message': f"User {user_id} added to group {group_id}"}), 200

@normal_route.route('/record_interaction_group', methods=['POST'])
def record_spot_interaction_group():
    """
    Record spot interactions for all users in a group if pressed_save is True.
    
    This endpoint accepts interaction data for a specific group and updates the 
    interactions for all group members in the database, only if 'pressed_save' is True.
    
    Returns:
        JSON response indicating the success or failure of the operation.
    """

    data = request.json

    # Data validation
   
    group_id = data.get('group_id')
    if not group_id:
        return jsonify({'error': 'Group ID is required'}), 400

    groups_collection = get_db()['Groups']
    
    try:
        # Find the group in the database
        group = groups_collection.find_one({'_id': group_id})
        if group is None:
            return jsonify({'error': 'Group not found'}), 404

        # Retrieve the list of user IDs from the group
        user_ids = group.get('members', [])
        if not user_ids:
            return jsonify({'error': 'No members found in the group'}), 404

        interactions = data.get('interaction', {})
        if not interactions:
            return jsonify({'error': 'No interaction data provided'}), 400

        # Prepare update data only for spots where 'pressed_save' is 'True'
        update_data = {
            '$set': {
                'last_active': datetime.now()
            }
        }

        # Filter interactions to only include those with 'pressed_save' set to 'True'
        for spot_id, interaction in interactions.items():
            if interaction.get('pressed_save') == "True":
                # Only record 'pressed_save' field
                update_data['$set'][f'location_specific.{spot_id}.pressed_save'] = "True"

        if len(update_data['$set']) == 1:  # Only 'last_active' was set, meaning no 'pressed_save' was True
            return jsonify({'message': 'No spots to update as pressed_save is not True for any spot'}), 200

        # Get the User collection to update each user
        user_collection = get_db()['User']

        # Update interactions for all group members
        for user_id in user_ids:
            # Check if user exists in the database
            if user_collection.find_one({'_id': int(user_id)}) is None:
                return jsonify({'error': f'User {user_id} not found'}), 404

            result = user_collection.update_one(
                {'_id': int(user_id)},
                update_data
            )

            if result.modified_count == 0:
                return jsonify({'error': f'No changes made for user {user_id}'}), 404

        return jsonify({'message': 'Interaction recorded successfully for all group members where pressed_save is True'}), 200

    except Exception as e:
        error_message = f"An error occurred while recording interactions: {str(e)}"
        print(error_message)  # Optional: log the error message
        return jsonify({'error': error_message}), 500
    
@normal_route.route('/clear_spot_data', methods=['GET'])
def clear_spot_data():
    """
    Clear spot data for a specific user.
    
    This endpoint accepts a user ID and clears all spot data for that user.
    
    Returns:
        JSON response indicating the success or failure of the operation.
    """
    
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    user_collection = get_db()['User']
    
    try:
        # Find the user in the database
        user = user_collection.find_one({'_id': int(user_id)})
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        
        # Clear all location-specific data for the user
        result = user_collection.update_one(
            {'_id': int(user_id)},
            {
                '$set': {
                    'location_specific': {}
                }
            }
        )
        
        if result.modified_count:
            return jsonify({'message': f"Spot data cleared for user {user_id}"}), 200
        else:
            return jsonify({'error': 'No changes made'}), 404
    
    except Exception as e:
        error_message = f"An error occurred while clearing spot data: {str(e)}"
        print(error_message)
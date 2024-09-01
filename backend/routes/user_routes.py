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
# Works perfectly fine, Validation works 
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

# Works perfectly fine 
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

    db = current_app.config['db']
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
    # print('vector:',sum(user_vector))
    # print('in loop:')
    # for i in range(len(user_vector)):
    #     print('iter:',i)
    #     if user_vector[i] != 0:
    #         print(i,":",user_vector[i], end='\t')
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


    
# Validation good 
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
    
    db = current_app.config['db']
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

    db = current_app.config['db']
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
@normal_route.route('/get_next_spot', methods=['GET'])
def get_next_spot():
    user_id = request.args.get('user_id')
    next_spot = get_next_items(user_id)
    db = current_app.config['db']
    user = db['User']
    try:
        user_id = int(user_id)
    except:
        pass
    # vector_db = db['UserVectors']
    # vector= vector_db.find_one({'_id': user_id})['vector']
    # print('vector:',sum(vector))
    # print('in loop:')
    # for i in range(len(vector)):
    #     print('iter:',i)
    #     if vector[i] != 0:
    #         print(i,":",vector[i], end='\n')
    # print(f'\n\nuser_vector{sum(vector)}\n\n')
    ret = []
    seen = list(user.find_one({'_id': user_id}).get('location_specific', {}).keys())
    
    if not next_spot:
        return jsonify({'message': 'No more spots available'}), 404
    
    for id in next_spot:
        # print (id, end = "\n")
        if id not in seen:
            ret.append(id)
    
    if ret:
        return jsonify(ret), 200
    
    return jsonify({'message': 'No more spots available'}), 404

@normal_route.route('/retrieve_current_preferences', methods=['GET'])
def retrieve_user_preferences():
    user_id = request.args.get('user_id')
    db = current_app.config['db']
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
    # schema = SpotListSchema()
    # ADD VALIDATION
    # try:
    #     # Validate the input data
    #     data = schema.load(request.json)
    # except ValidationError as err:
    #     return jsonify(err.messages), 400
    data = request.json
    # Extract the list of spot IDs
    spotLists = data['spotLists']

    # Connect to the database
    db = current_app.config['db']
    spots = db['Spot']

    # Query to find documents with the specified IDs
    query = {"_id": {"$in": spotLists}}
    results = list(spots.find(query))

    # Optionally, you could serialize the results using Marshmallow
    return jsonify(results), 200



@normal_route.route('/get_group_spot', methods=['GET'])
def get_next_group_spot():
    user_ids = request.args.getlist('user_ids')
    # print('\n\n user_ids:',user_ids,'\n\n')
    group_spot = get_group_recommendation(user_ids)
    
    if group_spot is not None:
        return jsonify(group_spot), 200
    else:
        return jsonify({'message': 'No group spot available'}), 404


@normal_route.route('/create_group', methods=['POST'])
def create_group():
    data = request.json
    group_id = data.get('group_id')
    groups = current_app.config['db']['Group']
    groups.insert_one({
        '_id': group_id,
        'members': [data.get('creator')]
    })
    return jsonify({'group created': group_id}), 200



@normal_route.route('/add_to_group', methods=['POST'])
def add_to_group():
    data = request.json
    group_id = data.get('group_id')
    user_id = data.get('user_id')
    groups = current_app.config['db']['Group']
    groups.update_one(
        {'_id': group_id},
        {
            '$addToSet': {
                'members': user_id
            }
        }
    )
    return jsonify({'message': f"User {user_id} added to group {group_id}"}), 200




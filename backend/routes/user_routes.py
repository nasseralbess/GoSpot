from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime
from helpers import get_next_items, get_group_recommendation
from schemas.user_schema import UserInteractionSchema, UserSchema, UpdatePreferencesSchema

# Initialistion 
normal_route = Blueprint('normal_routes', __name__)

# Schemas 
user_interaction_schema = UserInteractionSchema()
adding_user_schema = UserSchema()
updating_preferences = UpdatePreferencesSchema()

# Adds a user, and fail if user already exists
# Works perfectly fine, Validation works 
@normal_route.route('/add-user', methods=['POST'])
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
        'friends': [],
        'name': data.get('name'),
        'password': data.get('password'),
        'age': data.get('age'),
        'last_active': datetime.now()
    }

    user.insert_one(new_user)
    return jsonify({'message': f"New user {user_id} added successfully"}), 201

# Works perfectly fine 
# Updates the entire preferences
@normal_route.route('/update-preferences', methods=['PUT'])
def update_user_preferences():
    data = request.json

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

    if result.modified_count:
        return jsonify({'message': f"Preferences updated for user {user_id}"}), 200
    else:
        return jsonify({'error': 'User not found or no changes made'}), 404


    
# Validation good 
# Recording interactions of places for users 
@normal_route.route('/record-interaction', methods=['POST'])
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
@normal_route.route('/update-coordinates', methods=['PUT'])
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

# Adding a new friend 
# Additional validation where it checks if both users exists 
@normal_route.route('/add-friend', methods=['POST'])
def add_friend():
    db = current_app.config['db']
    user = db['User']

    user_to_add = request.args.get('friend')
    
    current_user = request.args.get('user')

    if not user_to_add or not current_user:
        return jsonify({'error': 'User and friend information must be provided'}), 400

    # Check if users exists in the database
     # Check if both users exist in the database
    if not user.find_one({'_id': int(current_user)}):
        return jsonify({'error': f'User {current_user} does not exist'}), 404
    
    if not user.find_one({'_id': int(user_to_add)}):
        return jsonify({'error': f'Friend {user_to_add} does not exist'}), 404


    result = user.update_one(
        {'_id': int(current_user)},
        {
            '$push': {
                'friends': int(user_to_add)
            }
        }
    )

    if result.modified_count:
        return jsonify({'message': f"Added friend for user {current_user}"}), 200
    else:
        return jsonify({'error': 'User not found or no changes made'}), 404



# Not working for string ids 
@normal_route.route('/get-next-spot', methods=['GET'])
def get_next_spot():
    #print("\n\n Here \n\n")
    user_id = request.args.get('user_id')
    #print("user_id:",user_id)
    next_spot = get_next_items(user_id)
    db = current_app.config['db']
    user = db['User']
    try:
        user_id = int(user_id)
    except:
        pass
    # print("\n\n\n\n\n\n")
    # print("Bread:",type(user_id))
    # print("\n\n Db:",db)   
    # print("\n\n\nfind_one:",user.find_one({'_id': 1}))
    seen = list(user.find_one({'_id': user_id}).get('location_specific', {}).keys())
    # print("\n\n\n\n\n\n")
    if next_spot is None:
        return jsonify({'message': 'No more spots available'}), 404
    for spot in next_spot:
        if spot not in seen:
            return jsonify(next_spot.to_dict()), 200
    
    return jsonify({'message': 'No more spots available'}), 404


@normal_route.route('/get-group-spot', methods=['GET'])
def get_next_group_spot():
    user_ids = request.args.getlist('user_ids')
    group_spot = get_group_recommendation(user_ids)
    
    if group_spot is not None:
        return jsonify(group_spot.to_dict()), 200
    else:
        return jsonify({'message': 'No group spot available'}), 404
    
# @normal_route.route('/add-friend', methods=['POST'])
# def add_friend():
#     print("request sent")
#     data = request.json
#     user_id = data.get('user_id')
#     friend_id = data.get('friend_id')

#     db = current_app.config['db']
#     user = db['User']

#     user.update_one(
#         {'_id': user_id},
#         {
#             '$addToSet': {
#                 'friends': friend_id
#             }
#         }
#     )

#     return jsonify({'message': f"Friend {friend_id} added for user {user_id}"}), 200
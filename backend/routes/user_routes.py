from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime
from helpers import get_next_items, get_group_recommendation

normal_route = Blueprint('normal_routes', __name__)

@normal_route.route('/add-user', methods=['POST'])
def add_new_user():
    data = request.json
    db = current_app.config['db']
    user = db['User']

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

@normal_route.route('/update-preferences', methods=['PUT'])
def update_user_preferences():
    data = request.json
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

@normal_route.route('/record-interaction', methods=['POST'])
def record_spot_interaction():
    data = request.json
    user_id = data.get('user_id')
    spot_id = data.get('spot_id')
    interaction = data.get('interaction')

    db = current_app.config['db']
    user = db['User']

    result = user.update_one(
        {'_id': user_id},
        {
            '$set': {
                f'location_specific.{spot_id}': interaction,
                'last_active': datetime.now()
            }
        }
    )

    if result.modified_count:
        return jsonify({'message': f"Interaction recorded for user {user_id} with spot {spot_id}"}), 200
    else:
        return jsonify({'error': 'User not found or no changes made'}), 404

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

@normal_route.route('/get-next-spot', methods=['GET'])
def get_next_spot():
    print("\n\n Here \n\n")
    user_id = request.args.get('user_id')
    print("user_id:",user_id)
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
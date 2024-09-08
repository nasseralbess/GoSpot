from flask import Blueprint, request, jsonify, current_app
from bson import ObjectId
from datetime import datetime
from helpers import *
from schemas.group_schema import GroupInteractionSchema, GroupSchema, addGroupSchema


# Initialistion 
group_route = Blueprint('group_routes', __name__)

#Group Schemas 
group_interaction_schema = GroupInteractionSchema()
adding_user_to_group_schema = addGroupSchema()
create_group_schema = GroupSchema() 




#
#
#Group Section
#
@group_route.route('/get_group_spot', methods=['GET'])
def get_next_group_spot():
    group_id = request.args.get('group_id')
    num_items = request.args.get('num_items', default=1, type=int)  # New query parameter to specify the number of items

    groups_collection = get_db()['Groups']
    try:
        group = groups_collection.find_one({'_id': group_id})
        if group is None:
            return jsonify({'error': 'Group not found'}), 404

        user_ids = group.get('members', [])
        
        group_spot = get_group_recommendation(user_ids, num_items)
    

        if group_spot is not None:
            return jsonify(group_spot), 200
        else:
            return jsonify({'message': 'No group spot available'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@group_route.route('/create_group', methods=['POST'])
def create_group():


    data = request.json
    
    errors = create_group_schema.validate(data)
    
    if errors:
        return jsonify({
            "message": "Data Structure Invalid, please ensure data structure is correct",
            "errors": (errors)
        }), 400
    
    
    group_id = data.get('group_id')
    group_name = data.get('group_name')
    groups = get_db()['Groups']
    groups.insert_one({
        '_id': group_id,
        'members': [data.get('creator')],
        'group_name': group_name
    })
    return jsonify({'group created': group_id}), 200



@group_route.route('/add_to_group', methods=['POST'])
def add_to_group():

        
    data = request.json

    errors = adding_user_to_group_schema.validate(data)
    
    if errors:
        return jsonify({
            "message": "Data Structure Invalid, please ensure data structure is correct",
            "errors": (errors)
        }), 400
    

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

@group_route.route('/record_interaction_group', methods=['POST'])
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
   
    errors = group_interaction_schema.validate(data)
    
    if errors:
        return jsonify({
            "message": "Data Structure Invalid, please ensure data structure is correct",
            "errors": (errors)
        }), 400
    
    groups_collection = get_db()['Groups']
    group_id = data.get('group_id')


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
    
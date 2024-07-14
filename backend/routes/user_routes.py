import json
from bson.objectid import ObjectId
from schemas.user_schema import InteractionSchema, RecordActivitySchema
from bson import json_util
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError


# Setup 
normal_route = Blueprint('normal_routes', __name__)
# Helper method 
def parse_json(data):
    return json.loads(json_util.dumps(data))
# For future schema validation 
record_activity_schema = RecordActivitySchema()



# teting routes 
@normal_route.route('/you', methods=['GET'])
def getUser():
    db = current_app.config['db']
    user = db['User']
    users = user.find_one({'name':'default'})
    return json_util.dumps(users)

#  Insrting a user based on 

# Insertin a user
@normal_route.route('/insert-user',methods=['POST'])
def insertUser():
    data = request.json
    # password should already by hashed
    db = current_app.config['db']
    user = db['User']
    # Starting data, so starting with no friends
    # Password should already be hashed 
    # Not sure if I should add validation for this
    user_data = {
        "name": data.get("name"),
        "password": data.get("password"),
        "age": data.get("age"),
        "country_origin": data.get("country_origin"),
        "friends":[],
        "location_specific": {},
        # all good
        "general_preferences": {
            "price": data.get("general_preferences", {}).get("price"),
            "categories": data.get("general_preferences", {}).get("categories"),
            "coordinates": data.get("general_preferences", {}).get("coordinates")
        }
    }
    result = user.insert_one(user_data)
    return jsonify({'status': 'Data inserted', 'id': str(result.inserted_id)}), 201


# The user has swiped 
# We will be creating it in five batches,
# In the client side we will do batching with localstorage 
# Possibly add some validation here
@normal_route.route("/swipe-information", methods=["POST"])
def addLocationPreferences():
    data = request.json
    update_user = request.args.get('user')  # User ID passed as query parameter


   
    # Validate the incoming data against the schema
    try:
        validated_data = record_activity_schema.load(data)
    except ValidationError as err:
        # If validation fails, return the errors
        return jsonify({'errors': err.messages}), 400


    db = current_app.config['db']
    all_users = db['User']
    actual_data = validated_data['interactions']

    # Preparing update document using dynamic $set operations for each key in the location_preferences
    update_operations = {"$set": {}}
    for key, preference in actual_data.items():
        update_operations["$set"][f"location_specific.{key}"] = preference
    print(update_operations)
    # Updating the user document to include new location specific preferences under their specific keys
    result = all_users.update_one(
        {"_id": ObjectId(update_user)},
        update_operations
    )

    if result.modified_count > 0:
        return jsonify({'status': 'Location preferences successfully added'}), 200
    else:
        return jsonify({'status': 'Update failed or no changes made'}), 400




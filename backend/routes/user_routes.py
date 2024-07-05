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

# Insertin a user
@normal_route.route('/insert-user',methods=['POST'])
def insertUser():
    data = request.json
    # password should already by hashed
    db = current_app.config['db']
    user = db['User']
    # Starting data, so starting with no friends
    # Password should already be hashed 
    user_data = {
        "name": data.get("name"),
        "password": data.get("password"),
        "age": data.get("age"),
        "country_origin": data.get("country_origin"),
        "friends":[],
        "interactions": [],
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
@normal_route.route("/swipe_information", methods=["POST"])
def swipedRight():
    data = request.json
    update_user = request.args.get('user')
   

    try:
        validated_data = record_activity_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
  
    # Inserting data
    swipe_data = validated_data['interactions']
    db = current_app.config['db']
    all_users = db['User']
    # return (swipe_data)
    result = all_users.update_one(
        {"_id":ObjectId( update_user)},
        {"$push": {"interactions": {"$each": swipe_data}}}
    )
    # return interactions
    if result.modified_count > 0:
        return jsonify({'status': 'Activities recorded'}), 200
    else:
        return jsonify({'status': 'No valid interactions found'}), 400


# Chang
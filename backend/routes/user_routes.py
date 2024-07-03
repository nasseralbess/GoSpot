import json
from bson import json_util
from flask import Blueprint, request, jsonify, current_app

normal_route = Blueprint('normal_routes', __name__)

def parse_json(data):
    return json.loads(json_util.dumps(data))

@normal_route.route('/you', methods=['GET'])
def getUser():
    db = current_app.config['db']
    user = db['User']
    users = user.find_one({'name':'default'})
    return json_util.dumps(users)


@normal_route.route('/inser-user',method=['POST'])
def insertUser():
    
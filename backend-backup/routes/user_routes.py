from flask import Blueprint, request, jsonify
from pymongo import MongoClient

# Blueprint setup 1
user_route = Blueprint('example', __name__)

@user_route.route('/get-user', methods=['POST'])
def getUser():
    print("Yousef")

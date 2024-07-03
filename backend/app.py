from flask import Flask, request, jsonify
from pymongo import MongoClient
from routes.user_routes import normal_route
app = Flask(__name__)

# MongoDB Atlas connection string
# have to put these in config or .env ifles in the future
client = MongoClient('mongodb+srv://loko:melike2004@lovelores.h1nkog2.mongodb.net/?retryWrites=true&w=majority&appName=LoveLores')
db = client.GoSpot

# Make `db` available to blueprints
app.config['db'] = db

# register blueprint 
app.register_blueprint(normal_route, url_prefix='/home')

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("failed")
    print(e)

# @app.route('/')
# def index():
#     return "Welcome to the Flask MongoDB app!"

if __name__ == '__main__':
    app.run(debug=True)
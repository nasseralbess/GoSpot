from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from routes.user_routes import normal_route



import hashlib
# ONLY FOR TESTING PURPOSES 
from flask_wtf.csrf import CSRFProtect



app = Flask(__name__)
CORS(app)
# MongoDB Atlas connection string
# have to put these in config or .env ifles in the future
client = MongoClient('mongodb+srv://loko:melike2004@lovelores.h1nkog2.mongodb.net/?retryWrites=true&w=majority&appName=LoveLores')
db = client.GoSpot

# Make `db` available to blueprints
app.config['db'] = db

# TESTING PURPOSES 
csrf = CSRFProtect(app)
csrf.exempt(normal_route)
# register blueprint for users
app.register_blueprint(normal_route, url_prefix='/user')

# register bluepring for places


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
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Atlas connection string
client = MongoClient('mongodb+srv://loko:<melike2004>@lovelores.h1nkog2.mongodb.net/?retryWrites=true&w=majority&appName=LoveLores')

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
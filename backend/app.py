from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
import json
from bson import json_util
from pydantic import BaseModel

# initialisation 
app = FastAPI()

# setting up mongoDB connection 
client = MongoClient("mongodb+srv://noobylub:thispassword@lovelores.h1nkog2.mongodb.net/?retryWrites=true&w=majority&appName=LoveLores")
db = client.GoSpot
users = db.User

# Required as mongoDB is in BSON, and fastapi just said its too much to handle
def parse_json(data):
    return json.loads(json_util.dumps(data))


# pydantic classes to define against the body 
class User(BaseModel):
    name: str



# testing retrieval
@app.get("/")
async def root():
    foundUser = (users.find_one(ObjectId('66826eee6ac658e7e22048e3')))
    print(foundUser['name'])
    foundUser = parse_json(foundUser)
    return foundUser

# testing insertions
@app.get("/insert/")
async def inserting(name: str ='default',friendsList: list=[],placesReview:list=[]):
    users.insert_one({
        "name":name,
        "friendsList":friendsList,
        "placesReviewed":placesReview
    })

from urllib.parse import parse_qs
from flask import Flask,request,json,Blueprint
from flask_login import login_required
from pymongo import MongoClient
from ..token.tokenVerify import token_required
import ast

#Setting up the database and getting the drink collection
client = MongoClient(host='127.0.0.1',port=27017)
database = client['drink-up']
drink_collection = database['drink']

#Defining the blueprint for the file so that we would connect it to home.py
drink_bp = Blueprint('drink',__name__)

app = Flask(__name__)

@app.route('drink-up/drinks', methods = ['GET'])
@login_required
@token_required
def get_drinks():
    """Function that returns all drinks from database."""
    try:
         drink_data = parse_qs((request.query_string))
            
         if drink_data:
             #Getting all drinks that match with the query parameters
             drinks = {k:int(v) if isinstance(v,str) and v.isdigit() else v for k,v in drink_data.items()}
             
             #To find for the drink in the database
             found_drinks = drink_collection.find(drinks)
               
             if found_drinks.count > 0:
                return f'The number of drinks found {found_drinks.count}',200
             else:
                return 'No drink found',200
    except:
            return 'Bad Request',500

@app.route('drink-up/drinks/<drinkId>', methods = ['GET'])
@login_required
@token_required
def get_one_drink(drinkId):
    """
    Function to get a single a drink
    """
    if isinstance(drinkId,int):
        try:
           found_drink = drink_collection.find({id:drinkId})
           return 'The drink was successfully found',200
        except:
            return 'This drink does not exist',404

#Creating a middleware so that only admins can access the route to manage the drinks
@app.before_request
def before_request():
    data = ast.literal_eval(json.dumps(request.get_json()))
    if data['role'] == 'ADMIN':
        pass

def check_api_key():
    key = request.headers.get('X-API-Key')
    
    if key in keys:
        pass
    else:
        return "You are unathourized to view this page",401



@app.route('drink-up/update-drink/<drinkId>', methods = ['POST'])   
@login_required
@token_required
def update_drink(drinkId):
    """To update a specified drink

    Args:
        drinkId (Object): This is the id of the specified drink
    """
    try:
        try:
            data = ast.literal_eval(json.dumps(request.get_json())) 
        except:
            return 'There is no data given',400
        
        updated_drink = drink_collection.update_one({id:drinkId},data)
        
        if updated_drink.modified_count > 0:
            return 'The drink has been successfully modified',201
        else:
            return 'There was an error when updating the drink',500
    except:
        return "No drink was updated",500


@app.route('drink-up/delete-drink/<drinkId>' methods = ['DELETE'])
def delete_drink(userId):
    userId = request
from flask import Flask,json,request,Blueprint,jsonify
from flask_login import login_required
from pymongo import MongoClient
from urllib.parse import parse_qs
import ast

client = MongoClient(host='127.0.0.1',port=27017)
database = client['drink-up']
user_collection = database['user']

user_bp = Blueprint('user',__name__)

app = Flask(__name__)
@app.route('drink-up/users', methods = ['GET'])
@login_required       
def get_users():
    """
    Function for getting user
    """
    try:
        #To get the query parameters
        parameter = parse_qs(request.query_string)
        
        if parameter:
            #To covert the values to int
         params = {k: int(v) if isinstance(v,str) and v.isdigit() else v for k,v in parameter.items()}
        
         #To get the data that satisfies the query parameters
         data = user_collection.find(params)
        
         if data.count > 0:
            return json.dumps(data)
         else:
            return 'No records were found',404
        else:
            if user_collection.find().count < 0:
                return json.dumps(user_collection.find())
            else:
                return jsonify([])
    except:
        return "No queries were not given",500

@app.route('drink-up/update_user/<userId>', methods= ['POST'])
@login_required
def update_user(userId):
    """Function to update a user's data

    Args:
        userId (Object): It is a route parameter containing the id of the user 
    """
    try:
        try:
            data = ast.literal_eval(json.dumps(request.get_json()))
        except:
            return 'There is no data in the body',400
        
        #Updating the user data
        updated_user = user_collection.insert_one({id:int(userId)},data)
        
        #Checking if there was any updates
        if update_user.modified_count > 0:
            return 'The user has been successfully updated',201
        else:
            return 'There was no changes made to the user',500
    except:
        return 'The user could not be updated. Try again',500
    
    
@app.route('drink-up/delete/<userId>', methods = ['DELETE'])
@login_required
def delete_user(userId):
    """Function to delete a user

    Args:
        userId (Object): It is a route parameter containing the id of the user 
    """
    try:
        deleted_user = user_collection.delete_one({id:int(userId)})
            
        if deleted_user.deleted_count > 0:
             return 'The user has been successfully deleted',204
        else:
                return 'The user you want to delete cannot be found',404
    except:
            return 'There was an error when deleting the user',500
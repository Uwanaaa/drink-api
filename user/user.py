from flask import Flask,json,request,Blueprint,jsonify,render_template,redirect
from flask_login import login_required
from pymongo import MongoClient
from urllib.parse import parse_qs
from ..token.tokenVerify import token_required
import ast,hashlib

client = MongoClient(host='127.0.0.1',port=27017)
database = client['drink-up']
user_collection = database['user']

user_bp = Blueprint('user',__name__)

app = Flask(__name__)

@app.route('drink-up/signup', methods = ['POST'])   
def render_signup():
    """
    Renders the HTML template file 'signup-form.html' located in the 'static' folder when the '/drink-up/signup' route is accessed with the HTTP method 'POST'.

    Returns:
    - The rendered HTML template 'signup-form.html' as the response.
    """
    return render_template('../static/signup-form.html')

@app.route("drink-up/signup/submit", methods =['POST'])
def create_account():
    """

    This function defines a  route for creating a new user account. It receives a POST request with user data, hashes the password, saves the data to a MongoDB database, and returns a JSON response.

    :return: JSON response with status code 201 if user data is successfully saved to the database, or an error message with status code 500 if there is an error creating the user.
    """
    try:
        try:
            # Extract user data from the request form data
            name = request.form['name']
            password = request.form['password']
            age = request.form['age']
            role = request.form['role']
            
            # Hash the password using the SHA256 algorithm
            hashed_password = hashlib.sha256(password.encode).hexdigest()
        except:
            return "There is no data in the request", 400
        
        # Save the user data to the database
        database = user_collection.insert_one(name, hashed_password, age)
        
        # Check if the database response is a list and return the JSON output
        if isinstance(database, list):
            return jsonify([str(v) for v in database]), 201
        else:
            return jsonify(str(database)), 201
    except:
        return "Error creating the user. Try again", 500

@app.route('drink-up/users')
def render_form():
    return render_template('../static/find-users.html')
@app.route('drink-up/users/result', methods = ['GET'])
@login_required
@token_required    
def get_users():
    """
    Function for getting all users
    """
    try:
        #To get the query parameters
        parameter = request.args.get('filter')
        
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
                 user_data = json.dumps(user_collection.find())
                 return user_data, redirect('../static/list-of-user.html')
            else:
                return jsonify([])
    except:
        return "No queries were not given",500

@app.route('drink-up/update_user/<userId>', methods= ['POST'])
@login_required
@token_required
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
    
    
@app.route('drink-up/delete-user/<userId>', methods = ['DELETE'])
@login_required
@token_required
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
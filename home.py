import ast,secrets,string
from pymongo import MongoClient
from flask import Flask, jsonify,request,json
from urllib.parse import parse_qs

#client = MongoClient(the url for the mongodb server)
#database = client[the specific database]
#collection = database[the specific collection]

#generating api key
def generate_api_key():
   key = string.ascii_letters + string.digits
   return ''.join(secrets.choice(key) for _ in range(32))

app=Flask(__name__)

@app.route("drink-up/home", methods =['POST'])

def create_account():
    """Function for creating a new user"""
    
    try:
        try:
            #To get the convert the json to string
            data = ast.literal_eval(json.dumps(request.get_json()))
        except:
            return "There is no data in the request",400
        
        keys = collection.insert(generate_api_key())

        #To save the data to the database 
        database = collection.insert(data)
        
        #To check if the database is a list and return the json output 
        if isinstance(database,list):
            return jsonify([str(v) for v in database]),201
        else:
            return jsonify(str(database)),201
    except:
        return "Error creating the user. Try again",500

@app.route('drink-up/users', methods = ['GET'])
        
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
         data = collection.find(params)
        
         if data.count > 0:
            return json.dumps(data)
         else:
            return 'No records were found',404
        else:
            if collections.find().count < 0:
                return json.dumps(collections.find())
            else:
                return jsonify([])
    except:
        return "No queries were not given",500

@app.route('drink-up/update_user/<userId>', methods= ['POST'])
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
        updated_user = collection.insert_one({id:int(userId)},data)
        
        #Checking if there was any updates
        if update_user.modified_count > 0:
            return 'The user has been successfully updated',201
        else:
            return 'There was no changes made to the user',500
    except:
        return 'The user could not be updated. Try again',500

@app.route('drink-up/delete/<userId>', methods = ['DELETE'])
def delete_user(userId):
    """Function to delete a user

    Args:
        userId (Object): It is a route parameter containing the id of the user 
    """
    try:
        deleted_user = collection.delete_one({id:int(userId)})
            
        if deleted_user.deleted_count > 0:
             return 'The user has been successfully deleted',204
        else:
                return 'The user you want to delete cannot be found',404
    except:
            return 'There was an error when deleting the user',500

@app.errorhandler('404')
def page_not_found_error(e):
    """Function to send a message to the user in a case of status code 404

    Args:
        e (Object): It contain the status code 404
    """
    message = {
        'error':{
            'message': 'This route is not supported. Check the API Documentation.'
        }
    }
    response = jsonify(message)
    response.status_code = 404
    return response

@app.route('drink-up/drinks', methods = ['GET'])
def get_drinks():
    """Function that returns all drinks from database."""
    try:
         drink_data = parse_qs((request.query_string))
            
         if drink_data:
             #Getting all drinks that match with the query parameters
             drinks = {k:int(v) if isinstance(v,str) and v.isdigit() else v for k,v in drink_data.items()}
             
             #To find for the drink in the database
             found_drinks = collection.find(drinks)
               
             if found_drinks.count > 0:
                return f'The number of drinks found {found_drinks.count}',200
             else:
                return 'No drink found',200
    except:
            return 'Bad Request',500

@app.route('drink-up/drinks/<drinkId>', methods = ['GET'])
def get_one_drink(drinkId):
    """
    Function to get a single a drink
    """
    if isinstance(drinkId,int):
        try:
           found_drink = collection.find({id:drinkId})
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



@app.route('/drink-up/update-drink/<drinkId>', methods = ['POST'])   
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
        
        updated_drink = collection.insert({id:drinkId},data)
        
        if updated_drink.modified_count > 0:
            return 'The drink has been successfully modified',201
        else:
            return 'There was an error when updating the drink',500
    except:
        return "No drink was updated",500

    
if __name__ == '__main__':
    app.run()
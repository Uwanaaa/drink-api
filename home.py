import ast,secrets,string,hashlib
from flask import Flask, jsonify,request,json
from pymongo import MongoClient
from flask_login import login_required


#To connect our MongoDB database
client = MongoClient(host='127.0.0.1',port=27017)
database = client['drink-up']
drink_collection = database['drink']
user_collection = database['user']
key_collection = database['key']

#generating api key
def generate_api_key():
   key = string.ascii_letters + string.digits
   return ''.join(secrets.choice(key) for _ in range(32))

secret_key= secrets.token_hex(32)

app=Flask(__name__)
@app.route("drink-up/signup", methods =['POST'])

def create_account():
    """Function for creating a new user"""
    
    try:
        try:
            #To get the convert the json to string
            data = ast.literal_eval(json.dumps(request.get_json()))
            hashed_password = hashlib.sha256(data['password'].encode).hexdigest()
        except:
            return "There is no data in the request",400
        
        #To hash the api key for security and saving it in the database
        key = generate_api_key()
        keys = hashlib.sha256(key.encode).hexdigest()
        key_collection.insert_one(keys)
        

        #To save the data to the database 
        database = user_collection.insert_one(data['name',hashed_password,'email','age'])
        
        #To check if the database is a list and return the json output 
        if isinstance(database,list):
            return jsonify([str(v) for v in database]),201
        else:
            return jsonify(str(database)),201
    except:
        return "Error creating the user. Try again",500

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


@app.route('drink/create-drink')
@login_required


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

    
if __name__ == '__main__':
    app.run()
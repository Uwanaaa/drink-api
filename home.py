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
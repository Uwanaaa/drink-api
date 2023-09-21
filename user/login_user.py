from flask import Flask,request,json,redirect,Blueprint
from flask_login import LoginManager,current_user,UserMixin,login_required,login_user,logout_user
from pymongo import MongoClient
import ast,secrets

client = MongoClient(host= '127.0.0.1',port=27017)
database = client['drink-up']
user_collection = database['user']

secret_key= secrets.token_hex(32)

class User(UserMixin):
    def __init__(self,name,password):
        self.name = name
        self.password = password

login_user_bp = Blueprint('login-user',__name__)

app = Flask(__name__)

#Initializing the login manager
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('drink-up/login', methods = ['POST','GET'])
def login_user(name,password):
    if request.method == 'POST':
      data = ast.literal_eval(json.dumps(request.get_json()))
      name = data['name']
      password = data ['password']
      app.secret_key = secret_key
    
      if user_collection.find({'name':name}):
         user = user_collection.find({'name':name,'password':password})
         if user['password'] == password: 
            user = User(name,password)
            login_user(user)
            return redirect('drink-up/drinks')
         else:
            return "The password is not correct for this user"
      else:
        return "This user does not exists"
    else:
        #show the login form as the returned value
        #try using url_for('static',filename =)
        pass


@app.route('drink-up/logout')
def logout():
    logout_user()
    return f'Bye, {current_user.name}. See you later'

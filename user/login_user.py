from flask import Flask,request,redirect,Blueprint,url_for,jsonify
from flask_login import LoginManager,current_user,UserMixin,login_user,logout_user
from ..schema.schemaValidator import userSchema
from itsdangerous import TimedSerializer as Serializer
from pymongo import MongoClient

client = MongoClient(host= '127.0.0.1',port=27017)
database = client['drink-up']
user_collection = database['user']

#This class define stores logged in users and helps to log the user out 
class User(UserMixin):
    def __init__(self,name,password):
        self.name = name
        self.password = password

login_user_bp = Blueprint('login-user',__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = '9c9067e71bf805928274f84ccac61a8f'
#Initializing the login manager
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('drink-up/login', methods = ['POST','GET'])
def validateDate():
    #Get data from the HTML form
    data = request.form
    
    #Loading the schema to validate the data
    schema = userSchema()
    errors = schema.validate(data)
    
    #Response if there is an error
    if errors:
        return 'Validation error: ' + str(errors)
    else:
        return data
    
def login_user():
    if request.method == 'POST':
      data = validateDate()
      name = data.get('name')
      password = data.get('password')
    
      if user_collection.find({'name':name}):
         user = user_collection.find({'name':name,'password':password})
         if user['password'] == password: 
            user = User(name,password)
            login_user(user)
            serial = Serializer(app.config['SECRET_KEY'], expires_in=3600)#it is seconds
            token = serial.dumps({'username': name}).decode('utf-8')
            return 'This is working'
         else:
            return "The password is not correct for this user"
      else:
        return "This user does not exists"
    else:
        return url_for('/static',filename ='signup-form.html')


@app.route('drink-up/logout')
def logout():
    logout_user()
    return f'Bye, {current_user.name}. See you later'

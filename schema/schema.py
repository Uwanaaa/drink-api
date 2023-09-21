from pymongo import MongoClient 
from marshmallow import Schema,fields,validate
client = MongoClient(host ='127.0.0.1',port = 27017)
db = client['drink-up']
user_collection = db['user']
drink_collection = db['drink']

class userSchema(Schema):
    name = fields.String(required=True,validate=validate.Length(max=20))
    password = fields.String(required=True,validate=validate.Length(min=8))
    age = fields.Integer(required=True,validate=validate.Length(max=3))
    role = fields.String(default='USER')
    
class drinkSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    price = fields.Integer(required=True) 

class drinkImageSchema(Schema):
    filename = fields.String(required=True, validate=validate.Length(max=255))
    file_data = fields.Raw(required=True)
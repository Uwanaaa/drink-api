from itsdangerous import BadSignature,SignatureExpired,TimedSerializer as Serializer
from flask import request,jsonify,Flask
from functools import wraps

app = Flask(__name__)
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'The token is missing'}),401
        
        try:
            serial = Serializer(app.config['SECRET_KEY'])
            data = serial.load(token)
        except SignatureExpired:
            return jsonify({'message': 'The token has expired'}),401
        except BadSignature:
            return jsonify({'message': 'The token is invalid'}),401
        
        return f(*args, **kwargs)
        
    return wrapper
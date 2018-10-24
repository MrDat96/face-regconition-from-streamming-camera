from dotenv import load_dotenv
import os
from app import create_app
from flask import request, jsonify, abort, render_template, redirect, Blueprint

from app.routers.role_api import role_api
from app.routers.users_api import users_api
from app.routers.room_api import room_api
from app.routers.camera_api import camera_api
from app.routers.checkin_api import checkin_api
from app.routers.recognition_api import recognition_api

#from app.models.user import User

load_dotenv()
config_name = os.getenv("APP_SETTINGS")
app = create_app(config_name)

public = Blueprint('public', __name__)

@public.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@public.route('/user', methods=['POST', 'GET'])
def user():
    response = jsonify({
        'id': 'SE62120',
        'name': 'Ngo Thuc Dat'
    })
    response.status_code = 200
    return response
    

app.register_blueprint(public)
app.register_blueprint(role_api)
app.register_blueprint(users_api)
app.register_blueprint(room_api)
app.register_blueprint(camera_api)
app.register_blueprint(checkin_api)
app.register_blueprint(recognition_api)

if __name__ == '__main__':
    app.run('0.0.0.0', 5001)
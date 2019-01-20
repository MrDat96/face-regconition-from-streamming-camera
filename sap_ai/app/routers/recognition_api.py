from flask import request, jsonify, abort, render_template, redirect, Blueprint
from flask import Flask, request, Response
import jsonpickle
import json
import base64
from io import StringIO
import numpy as np
import cv2
from datetime import datetime 
from app.ai_modules.recognition import recognition
import sys
import os

from app.models.user import User

import mqtt.publisher as publisher 

recognition_api = Blueprint('recognition_api', __name__)

PATHDATA = os.getenv("IMAGES_STORE_PATH")
# route http posts to this method
@recognition_api.route('/recognition/detect', methods=['POST'])
def detect():
    r = request
    data = json.loads(r.data)

    print(type(data))
    img = data['img_encoded']
    #print(img)
    print(type(img))
    print(data['camera_ip'])
    # convert string of image data to uint8
    nparr = np.fromstring(base64.b64decode(img), np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    path = PATHDATA + "/" + datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg'
    cv2.imwrite(path, img)
    labels = recognition(path)
    # do some fancy processing here....

    checkUser = False
    label_detect = "Unknown"

    if (labels is not None):
        for label in labels:
            if User.isExist(label):
                label_detect = label
                checkUser = True
                print("START to PULISH")
                user = User.getUserById(label)
                message = { 'access_code': publisher.PERMISSION, 'message': publisher.PERMISSION_MESSAGE, 'user': {'user_id': label, 'user_name': user.first_name + ' ' + user.last_name}}
                print(message)
                # Write to log file
                with open(os.getenv("TEST_DATA_LOG_FILE"), 'a+') as out:
                    out.write( os.getenv("TEST_USER_ID") + "\t" + os.getenv("TEST_USER_NAME") + "\t" + datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + "\t 1 \t"  + user.first_name + ' ' + user.last_name  + '\n')
                # publisher.client_publish('hieu', json.dumps(message), hostname="192.168.43.40")
                break

    if (checkUser == False):
        message = { 'access_code': publisher.NO_PERMISSION, 'user': {'user_id': "Unknown"}}
        #Write to log file
        print(message)
        with open(os.getenv("TEST_DATA_LOG_FILE"), 'a+') as out:
            out.write( os.getenv("TEST_USER_ID") + "\t" + os.getenv("TEST_USER_NAME") + "\t" + datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + "\t 0 \t" + label_detect +  '\n')
        # publisher.client_publish('hieu', json.dumps(message), hostname="192.168.43.40")

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")
    
    #return "oke", 200

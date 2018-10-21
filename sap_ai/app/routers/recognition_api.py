from flask import request, jsonify, abort, render_template, redirect, Blueprint
from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
from datetime import datetime 
from app.ai_modules.recognition import recognition
import sys
import os

recognition_api = Blueprint('recognition_api', __name__)

PATHDATA = "./data/images_data/"
# route http posts to this method
@recognition_api.route('/recognition/detect', methods=['POST'])
def detect():
    r = request

    print(request.path)

    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    path = PATHDATA + datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg'
    cv2.imwrite(path, img)
    recognition(path)
    # do some fancy processing here....

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")
    
    return root_path, 200
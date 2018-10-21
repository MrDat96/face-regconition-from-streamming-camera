from fas_recognition import detection, feature_extraction, classification, image_utils
from PIL import Image

import cv2
import sys
import time
from datetime import datetime
import time 

import traceback
import logging
#Threading
from threading import Thread

import requests
import json

#cascPath = sys.argv[1]
DETECTING = False

def start_detection():
    global DETECTING
    video_capture = cv2.VideoCapture(0)
    #video_capture.open("rtsp://admin:abcd1234@192.168.162.29:554/Streaming/Channels/2")

    NUMBER_OF_TIME = 2 # FPS equal 20 / NUMBEROFTIME
    counter = 0 #

    #detector = detection.MTCNNDetector(thresholds=[0.8, 0.9, 0.9])
    detector = detection.SSDDetector(min_score=0.5, max_pixels=100000000)
    while True:
        try:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            counter+=1
            if (counter >= NUMBER_OF_TIME):
                # print("FPS: ", 20 / NUMBER_OF_TIME)
                counter = 0
                start_time = time.time()
                print(ret)
                faces = detector.detect(frame) #Cut face
                #print(f'Detection time: {time.time() - start_time}')

                if len(faces) >= 1 and not DETECTING:
                    path = "./data/" + datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg'
                    cv2.imwrite(path, frame)
                    recognite_frame(path)


                print(faces)
                if (len(faces) >= 1):
                    for (top, right, bottom, left) in faces:
                        cv2.rectangle(frame,(left, top), (right, bottom),  (0, 255, 0), 2)
 
                cv2.imshow('Video', frame)
        except Exception as e:
            print("Oops! This loop error, continue with another")
            frame = None
            #video_capture.open("rtsp://admin:abcd1234@192.168.162.29:554/Streaming/Channels/2")
            logging.error(traceback.format_exc())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


def recognite_frame(path):
    thread = Thread(target = server_detection, args=(path, ))
    thread.start()

def server_detection(pathImage):
    global DETECTING
    DETECTING = True
    print("Send ", pathImage, "To Server")
    addr = 'http://localhost:5000'
    #test_url = addr + '/api/test'
    test_url = addr + '/recognition/detect'

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    img = cv2.imread(pathImage)
    # encode image as jpeg
    _, img_encoded = cv2.imencode('.jpg', img)
    # send http request with image and receive response
    response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
    # decode response
    #print(json.loads(response.text))
    print("Sent to server")
    time.sleep(5)
    DETECTING = False


if __name__ == "__main__":
    #recognition("./imageDetection.jpg")
    start_detection()
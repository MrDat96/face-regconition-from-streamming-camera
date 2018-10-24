#import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.publish as publish

NO_PERMISSION = 0
PERMISSION = 1
UNRECOGNITION = 2
SERVER_ERROR = 3

NO_PERMISSION_MESSAGE = "No permission"
PERMISSION_MESSAGE = "permission"
UNRECOGNITION_MESSAGE = "unrecognition"
SERVER_ERROR_MESSAGE = "server_error"

def client_publish(topic="sap", message="{'access_code': 1}", hostname=None):
    #message code : 0: no permission, 1: permission, 3: unregconition, 4: server error
    #publish.single(topic, "{ 'access_code': 1, 'permission': True, 'describe': 'permission', 'mac_address': '2d5h2f3gf23s3f' ,'user': { 'user_id': 'SE62120', 'user_name': 'Ngo Thuc Dat'}}", hostname="localhost")
    publish.single(topic, message, hostname=hostname)


if __name__ == "__main__":
    print("Start")
    client_publish()
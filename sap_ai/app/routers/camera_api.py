from flask import request, jsonify, abort, render_template, redirect, Blueprint
from app.models.camera import Camera
from app.models.room import Room

camera_api = Blueprint('camera_api', __name__)
# View all role with action
@camera_api.route('/cameras/view_all')
@camera_api.route('/cameras/<action>/<camera_id>', methods=['GET'])
def viewAllCameras(action="view_all", camera_id=""):
    if (action == "view_all"):
        cam_room = Camera.get_all_with_room()
        print(cam_room)
        message = ""
        return render_template('view_all_cameras.html', cam_room=cam_room, message = message)
    elif (action == "delete" and camera_id != ""):
        camera = Camera.get_camera_by_id(camera_id=camera_id)
        try:
            camera.delete() 
            message = 'Delete successful'
        except Exception as e:
            print(e)
            message='Delete User Error! Please try again!'
        return redirect("/cameras/view_all")

# Add a new Role
@camera_api.route('/cameras/add_new', methods=['GET', 'POST'])
def addNewCamera():
    message = ""
    rooms = Room.get_all()
    print(rooms)
    if request.method == 'POST':
        try:
            form = request.form
            camera_id = form['camera_id']
            camera_name = form['camera_name']
            camera_type = form['camera_type']
            camera_http_gateway = form['camera_http_gateway']
            camera_http_port = form['camera_http_port']
            camera_rtsp_gateway = form['camera_rtsp_gateway']
            camera_rtsp_port = form['camera_rtsp_port']
            camera_room_id = form['camera_room_id']
            print(camera_id, camera_name, camera_type, camera_http_gateway, camera_http_port, camera_rtsp_gateway, camera_rtsp_port, camera_room_id)
            
            if (camera_id == ""):
                message = "Camera ID cannot be empty"
            if (camera_name == ""):
                message += "\Camera name cannot be empty"
            if (camera_type == ""):
                message += "\Camera Type cannot be empty"
            if (camera_http_gateway == ""):
                message += "\nHttp Gateway cannot be empty"
            if (camera_http_port == ""):
                message += "\nHttp port cannot be empty"
            if (camera_rtsp_gateway == ""):
                message += "\nRtsp Gateway cannot be empty"
            if (camera_rtsp_port == ""):
                message += "\nRtsp port cannot be empty"
            if (camera_room_id == ""):
                message += "\nRoom cannot be empty"
            if (message == ""):
                camera = Camera(camera_id, camera_name, camera_type, camera_http_gateway, camera_http_port, camera_rtsp_gateway, camera_rtsp_port, camera_room_id)
                camera.save()
                message = "Save successful!"
        except Exception as e:
            print(e)
            message='Save role error! Please try again!'
    return render_template('add_camera.html', page_name="Add a camera", message=message, rooms=rooms)


# Edit a new Role
@camera_api.route('/cameras/edit/<camera_id>', methods=['GET', 'POST'])
def editCamera(camera_id = 0):

    message = ""
    rooms = Room.get_all()
    camera = Camera.get_camera_by_id(camera_id=camera_id)
    print(rooms)
    print(camera)
    if request.method == 'POST':
        try:
            form = request.form
            camera_id = form['camera_id']
            camera_name = form['camera_name']
            camera_type = form['camera_type']
            camera_http_gateway = form['camera_http_gateway']
            camera_http_port = form['camera_http_port']
            camera_rtsp_gateway = form['camera_rtsp_gateway']
            camera_rtsp_port = form['camera_rtsp_port']
            camera_room_id = form['camera_room_id']
            print(camera_id, camera_name, camera_type, camera_http_gateway, camera_http_port, camera_rtsp_gateway, camera_rtsp_port, camera_room_id)
            
            if (camera_id == ""):
                message = "Camera ID cannot be empty"
            if (camera_name == ""):
                message += "\Camera name cannot be empty"
            if (camera_type == ""):
                message += "\Camera Type cannot be empty"
            if (camera_http_gateway == ""):
                message += "\nHttp Gateway cannot be empty"
            if (camera_http_port == ""):
                message += "\nHttp port cannot be empty"
            if (camera_rtsp_gateway == ""):
                message += "\nRtsp Gateway cannot be empty"
            if (camera_rtsp_port == ""):
                message += "\nRtsp port cannot be empty"
            if (camera_room_id == ""):
                message += "\nRoom cannot be empty"
            if (message == ""):
                camera = Camera(camera_id, camera_name, camera_type, camera_http_gateway, camera_http_port, camera_rtsp_gateway, camera_rtsp_port, camera_room_id)
                camera.save()
                message = "Save successful!"
        except Exception as e:
            print(e)
            message='Save role error! Please try again!'
    return render_template('edit_camera.html', page_name="Edit camera", message=message, rooms=rooms, camera=camera)
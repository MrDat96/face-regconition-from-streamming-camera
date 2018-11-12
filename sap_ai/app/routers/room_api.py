from flask import request, jsonify, abort, render_template, redirect, Blueprint
from app.models.room import Room

room_api = Blueprint('room_api', __name__)
# View all role with action
@room_api.route('/rooms/view_all')
@room_api.route('/rooms/<action>/<room_id>', methods=['GET'])
def viewAllRoom(action="view_all", room_id=""):
    if (action == "view_all"):
        rooms = Room.get_all()
        message = ""
        return render_template('view_all_rooms.html', page_name="View all rooms", rooms=rooms, message = message)
    elif (action == "delete" and room_id != ""):
        print("Delete hehe")
        room = Room.get_room_by_id(room_id=room_id)
        try:
            room.delete() 
            message = 'Delete successful'
        except Exception as e:
            print(e)
            message='Delete Room Error! Please try again!'
        return redirect("/rooms/view_all")

# Add a new Role
@room_api.route('/rooms/add_new', methods=['GET', 'POST'])
def addNewRoom():
    message = ""
    if request.method == 'POST':
        try:
            form = request.form
            room_id = form['room_id']
            room_name = form['room_name']
            room_position = form['room_position']
            room_building = form['room_building']

            print(room_id, room_name, room_position, room_building)
            
            if (room_id == ""):
                message = "Room ID cannot be empty"
            if (room_name == ""):
                message += "\nRoom name cannot be empty"
            if (room_position == ""):
                message += "\nRoom Postion cannot be empty"
            if (room_building == ""):
                message += "\nRoom Building of birth cannot be empty"
            if (message == ""):
                room = Room(room_id, room_name, room_position, room_building)
                room.save()
                message = "Save successful!"
        except Exception as e:
            print(e)
            message='Save room error! Please try again!'
    return render_template('add_room.html', page_name="Add a room", message=message)


# Edit a new Role
@room_api.route('/rooms/edit/<room_id>', methods=['GET', 'POST'])
def editRoom(room_id = 0):

    message = ""
    room = Room.get_room_by_id(room_id=room_id)

    if request.method == 'POST':
        try:
            form = request.form
            room_id = form['room_id']
            room_name = form['room_name']
            room_position = form['room_position']
            room_building = form['room_building']

            print(room_id, room_name, room_position, room_building)
            
            if (room_id == ""):
                message = "Room ID cannot be empty"
            if (room_name == ""):
                message += "\nRoom name cannot be empty"
            if (room_position == ""):
                message += "\nRoom Postion cannot be empty"
            if (room_building == ""):
                message += "\nRoom Building of birth cannot be empty"
            if (message == ""):
                room.room_id = room_id
                room.name = room_name
                room.position = room_position
                room.building = room_building
                room.save()
                message = "Save successful!"
        except Exception as e:
            print(e)
            message='Save room error! Please try again!'

    return render_template('edit_room.html', page_name="Edit room", room=room, message=message)
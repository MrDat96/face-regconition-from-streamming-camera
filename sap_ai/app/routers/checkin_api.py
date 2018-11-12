from flask import request, jsonify, abort, render_template, redirect, Blueprint
from app.models.camera import Camera
from app.models.user import User
from app.models.checkin_status import CheckInStatus
from app.models.checkin import CheckIn

from datetime import datetime

checkin_api = Blueprint('checkin_api', __name__)
# View all role with action
@checkin_api.route('/checkin/view_all')
@checkin_api.route('/checkin/<action>/<int:checkin_id>', methods=['GET'])
def viewAllCheckin(action="view_all", checkin_id=""):
    if (action == "view_all"):
        checkins = CheckIn.get_all_with_user_camera_status() # Get a list of Check In with Foregin key User, Camera and CheckInStatus
        #print(checkins)
        message = ""
        return render_template('view_all_checkins.html', page_name="View all check in", checkins=checkins, message = message)
    elif (action == "delete" and checkin_id != ""):
        checkin = CheckIn.getUserById(checkin_id=usercheckin_id_id)
        try:
            checkin.delete() 
            message = 'Delete successful'
        except Exception as e:
            print(e)
            message='Delete User Error! Please try again!'
        return redirect("/checkin/view_all")


@checkin_api.route('/checkin/generate')
def generateCheckIn():
    # checkin_status = CheckInStatus(1, "Success")
    # checkin_status.save()
    # checkin_status = CheckInStatus(2, "Fail")
    # checkin_status.save()

    checkin_status = CheckInStatus.getCheckInStatus(1)
    checkin_status.name = "Success"
    checkin_status.save()
    checkin_status = CheckInStatus.getCheckInStatus(2)
    checkin_status.name = "Fail"
    checkin_status.save()

    # checkin = CheckIn(user_id="SE62120", camera_id=3, time_stamp = datetime.now(), checkin_status_id = 1)
    # checkin.save()
    return "Success", 200
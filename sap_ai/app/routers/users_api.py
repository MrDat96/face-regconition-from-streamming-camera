from flask import request, jsonify, abort, render_template, redirect, Blueprint
from app.models.role import Role
from app.models.user import User

users_api = Blueprint('users_api', __name__)
# View all role with action
@users_api.route('/users/view_all')
@users_api.route('/users/<action>/<user_id>', methods=['GET'])
def viewAllUsers(action="view_all", user_id=""):
    if (action == "view_all"):
        users = User.get_all_with_Role()
        message = ""
        return render_template('view_all_users.html', users=users, message = message)
    elif (action == "delete" and user_id != ""):
        user = User.getUserById(user_id=user_id)
        try:
            user.delete() 
            message = 'Delete successful'
        except Exception as e:
            print(e)
            message='Delete User Error! Please try again!'
        return redirect("/users/view_all")

# Add a new Role
@users_api.route('/users/add_new', methods=['GET', 'POST'])
def addNewUser():
    message = ""
    roles = Role.get_all()
    if request.method == 'POST':
        try:
            form = request.form
            user_id = form['user_id']
            user_first_name = form['user_first_name']
            user_last_name = form['user_last_name']
            user_date_of_birth = form['user_date_of_birth']
            user_role_id = form['user_role_id']
            user_occupancy = form['user_occupancy']
            print(user_id, user_first_name, user_last_name, user_date_of_birth, user_role_id, user_occupancy)
            
            if (user_id == ""):
                message = "User ID cannot be empty"
            if (user_first_name == ""):
                message += "\nFirst name cannot be empty"
            if (user_last_name == ""):
                message += "\nLast cannot be empty"
            if (user_date_of_birth == ""):
                message += "\nDate of birth cannot be empty"
            if (message == ""):
                user = User(user_id, user_first_name, user_last_name, user_date_of_birth, user_role_id, user_occupancy)
                user.save()
                message = "Save successful!"
        except Exception as e:
            print(e)
            message='Save role error! Please try again!'
    return render_template('add_user.html', message=message, roles=roles)


# Edit a new Role
@users_api.route('/users/edit/<user_id>', methods=['GET', 'POST'])
def editUser(user_id = 0):

    message = ""
    user, user_role = User.getUserWithRoleById(user_id=user_id)[0]
    roles = Role.get_all()
   
    if request.method == 'POST':
        try:
            form = request.form
            user_id = form['user_id']
            user_first_name = form['user_first_name']
            user_last_name = form['user_last_name']
            user_date_of_birth = form['user_date_of_birth']
            user_role_id = form['user_role_id']
            user_occupancy = form['user_occupancy']
            print(user_id, user_first_name, user_last_name, user_date_of_birth, user_role_id, user_occupancy)
            
            if (user_id == ""):
                message = "User ID cannot be empty"
            if (user_first_name == ""):
                message += "\nFirst name cannot be empty"
            if (user_last_name == ""):
                message += "\nLast cannot be empty"
            if (user_date_of_birth == ""):
                message += "\nDate of birth cannot be empty"
            if (message == ""):
                user.user_id = user_id
                user.first_name = user_first_name
                user.last_name = user_last_name
                user.date_of_birth = user_date_of_birth
                user.role_id = user_role_id
                user.occupancies = user_occupancy
                user.save()
                message = "Save successful!"
        except Exception as e:
            print(e)
            message='Update user rrror! Please try again!'

    return render_template('edit_user.html', user = user, roles=roles, user_role = user_role, message=message)
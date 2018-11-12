from flask import request, jsonify, abort, render_template, redirect, Blueprint
from app.models.role import Role

role_api = Blueprint('api', __name__)
# View all role with action
@role_api.route('/role/view_all')
@role_api.route('/role/<action>/<int:role_id>', methods=['GET'])
def viewAllRoute(action="view_all", role_id=0):

    role = Role.getRoleById(role_id=role_id)
    if (action == "view_all"):
        roles = Role.get_all()
        message = "None"
        return render_template('view_all_role.html', page_name="View all role", roles=roles, message = message)
    elif (action == "edit" and role_id != 0):
        return render_template('edit_role.html', role=role)
    elif (action == "delete" and role_id != 0):
        try:
            role.delete()
            message = 'Delete successful'
        except Exception as e:
            print(e)
            message='Delete Role Error! Please try again!'
        return redirect("/role/view_all")

        
    
# Add a new Role
@role_api.route('/role/add_new', methods=['GET', 'POST'])
def addNewRole():
    message = ""
    if request.method == 'POST':
        try:
            form = request.form
            role_name = form['role_name']
            role_power = form['role_power']
            role = Role(role_name, role_power)
            if (role_name == ""):
                message = "Name cannot Empty!"
            elif role.exists():
                message = "Name existed!"
            else:
                role.save()
                message='Save successful'
        except Exception as e:
            print(e)
            message='Save Role Error! Please try again!'
    return render_template('add_role.html', page_name="Add role", message=message)

    
# Edit a new Role
@role_api.route('/role/edit/<role_id>', methods=['GET', 'POST'])
def editRole(role_id = 0):

    message = ""
    role = Role.getRoleById(role_id=role_id)
    print(role.role_id)
   
    if request.method == 'POST':
        try:
            form = request.form
            role_name = form['role_name']
            role_power = form['role_power']

            if (role_name == ""):
                message = "Name cannot Empty!"
            elif (role_name != role.name and Role.isExist(role_name)):
                message = "Name is Existed"
            else:
                role.name = role_name
                role.power = role_power
                role.save()
                message='Updated successful'
        except Exception as e:
            print(e)
            message='Update Role Error! Please try again!'

    return render_template('edit_role.html', page_name="Edit role", role = role, message=message)
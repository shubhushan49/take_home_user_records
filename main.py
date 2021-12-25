from flask import Flask, request
from helper_functions import *

app = Flask(__name__)

@app.route("/users", methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    #GET
    if request.method == "GET":
        #usage localhost:5000/users?user_id=x
        user_id = request.args.get('user_id')
        #if user id is not given in the get request return
        if user_id == None:
            return response(404, None)
        #fetch user if it exists in the database
        user = user_get(user_id)
        if user == None:
            return response(404, None)
        else:
            return response(200, user)
    #POST
    elif request.method == "POST":
        payload = json.loads(request.data)
        #incomplete/invalid json data
        if not validate_user_record(payload):
            return response(400, None)
        user = user_post(payload)
        #if a user exists
        if user == None:
            return response(409, None)
        else:
            return response(201, user)
    #PUT
    elif request.method == "PUT":
        payload = json.loads(request.data)
        #incomplete/invalid json data
        if not validate_user_record(payload):
            return response(409, None)
        user = user_put(payload)
        #user does not exist
        if user == None:
            return response(404, None)
        else:
            return response(200, user)
    #DELETE
    elif request.method == "DELETE":
        payload = json.loads(request.data)
        #incomplete/invalid json data
        if not validate_user_record(payload):
            return response(409, None)    
        user = user_delete(payload)
        #user does not exist
        if user == None:
            return response(404, None)
        else:
            return response(204, user)

@app.route("/groups", methods=['GET', 'POST', 'PUT', 'DELETE'])
def groups():
    if request.method == "GET":
        #usage  localhost:5000/groups?group_id=x
        group_id = request.args.get('group_id')
        #check if group is provided in the get request
        if group_id == None:
            return response(404, None)
        
        #fetch the group if it exists
        group = group_get(group_id)
        if group == None:
            return response(404, None)
        else:
            return response(200, group)
    elif request.method == "POST":
        group_post()
    elif request.method == "PUT":
        group_put()
    elif request.method == "DELETE":
        group_delete()

if __name__ == "__main__":
    app.run(debug=True)
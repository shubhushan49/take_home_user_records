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
            return None, 404
        #fetch user if it exists in the database
        user = user_get(user_id)
        if user == None:
            return None, 404
        else:
            return json.dumps({"data": user}), 200
    #POST
    elif request.method == "POST":
        payload = json.loads(request.data)
        #incomplete/invalid json data
        if not validate_user_record(payload):
            return None, 400
        user = user_post(payload)
        #if a user exists
        if user == None:
            return None, 409
        else:
            return json.dumps({"data": user}), 201
    #PUT
    elif request.method == "PUT":
        payload = json.loads(request.data)
        #incomplete/invalid json data
        if not validate_user_record(payload):
            return None, 409
        user = user_put(payload)
        #user does not exist
        if user == None:
            return None, 404
        else:
            return json.dumps({"data": user}), 200
    #DELETE
    elif request.method == "DELETE":
        payload = json.loads(request.data)
        #incomplete/invalid json data
        if not validate_user_record(payload):
            return None, 409
        user = user_delete(payload)
        #user does not exist
        if user == None:
            return None, 404
        else:
            return json.dumps({"data": user}), 204

@app.route("/groups/<group_name>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def groups(group_name):
    #check if group_name is provided in the url
    if len(group_name) == 0:
        return None, 404
        
    if request.method == "GET":
        #fetch the group if it exists
        group_members = group_get(group_name)
        if group_members == None:
            return None, 404
        else:
            return json.dumps({"users": group_members})
    elif request.method == "POST":
        group = group_post(group_name)
        if group == None:
            return None, 409
        else:
            return json.dumps({"users": []}), 201
    elif request.method == "PUT":
        #{"users": [mem1, mem2]}
        members = json.loads(request.data)["users"]
        updated_members = group_put(group_name, members)
        if updated_members == None:
            return None, 409
        else:
            return json.dumps({"users": updated_members}), 200
    elif request.method == "DELETE":
        data = group_delete(group_name)
        if data == None:
            return None, 404
        return json.dumps({"users":[]}), 204

if __name__ == "__main__":
    app.run(debug=True)
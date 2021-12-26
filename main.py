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
            return {}, 404, set_json_header()
        #fetch user if it exists in the database
        user, groups = user_get(user_id)
        if user == None:
            return {}, 404, set_json_header()
        else:
            print({"data": user_schema(user, groups)})
            return json.dumps({"data": user_schema(user, groups)}), 200, set_json_header()
    #POST
    elif request.method == "POST":
        payload = json.loads(request.data)
        #incomplete/invalid json data
        if not validate_user_record(payload):
            return {}, 400, set_json_header()
        user = user_post(payload)
        #if a user exists
        if user == None:
            return {}, 409, set_json_header()
        else:
            return json.dumps({"data": user_schema(user, payload['groups'])}), 201, set_json_header()
    #PUT
    elif request.method == "PUT":
        payload = json.loads(request.data)
        #incomplete/invalid json data
        if not validate_user_record(payload):
            return {}, 409, set_json_header()
        user, groups = user_put(payload)
        #user does not exist
        if user == None:
            return {}, 404, set_json_header()
        else:
            return json.dumps({"data": user_schema(user, groups)}), 200, set_json_header()
    #DELETE
    elif request.method == "DELETE":
        payload = json.loads(request.data)
        if payload.get('id') == None:
            return {}, 409, set_json_header()
        # data {"id": "username"}
        user, groups = user_delete(payload.get('id'))
        #user does not exist
        if user == None:
            return {}, 404, set_json_header()
        else:
            return json.dumps({"data": user_schema(user, groups)}), 204, set_json_header()

@app.route("/groups/<group_name>", methods=['GET', 'POST', 'PUT', 'DELETE'])
def groups(group_name):
    #check if group_name is provided in the url
    if len(group_name) == 0:
        return {}, 404, set_json_header()
    if request.method == "GET":
        #fetch the group if it exists
        group_members = group_get(group_name)
        if group_members == None:
            return {}, 404, set_json_header()
        else:
            return json.dumps({"users": group_members})
    elif request.method == "POST":
        group = group_post(group_name)
        if group == None:
            return {}, 409, set_json_header()
        else:
            return json.dumps({"users": []}), 201
    elif request.method == "PUT":
        #{"users": [mem1, mem2]}
        members = json.loads(request.data)["users"]
        updated_members = group_put(group_name, members)
        if updated_members == None:
            return {}, 409, set_json_header()
        else:
            return json.dumps({"users": updated_members}), 200
    elif request.method == "DELETE":
        data = group_delete(group_name)
        #if group does not exist
        if data == None:
            return {}, 404, set_json_header()
        return json.dumps({"users":[]}), 204

if __name__ == "__main__":
    app.run(debug=True)
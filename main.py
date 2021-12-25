from flask import Flask
from helper_functions import *
from database_helper import session, User, Group, UserAndGroup

app = Flask(__name__)

@app.route("/users")
def users():
    return "<h1>Users/h1>"

@app.route("/group")
def groups():
    return "<h1>Groups</h1>"

if __name__ == "__main__":
    app.run(debug=True)
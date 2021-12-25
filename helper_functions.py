from database_helper import session, User, Group, UserAndGroup
from sqlalchemy.sql.expression import and_
import json
#response object
def response(status, data):
    return json.dumps({"status": status, "data": data})
#checks if the json payload is valid
def validate_user_record(record):
    valid_entry = 4
    for key in record.keys():
        if key == "first_name" or key == "last_name" or key == "id" or key == "groups":
            valid_entry -= 1
    
    if valid_entry == 0:
        return True
    else:
        return False
#Deletes users and associations to groups from the database
def user_delete(user_id):
    #fetch user
    user = session.query(User).filter(User.user_id == user_id).first()
    #check if user exists
    if user == None:
        return None
    #fetch all the groups that the user belongs to
    users_and_groups = session.query(UserAndGroup).filter(UserAndGroup.user_id == user.id)
    #delete the relationship between user and groups they belonged to
    for item in users_and_groups:
        session.delete(item)
        session.commit()
    #delete the user
    session.delete(user)
    session.commit()
    return user

#fetches user from the database
def user_get(user_id):
    #fetch user from database
    user = session.query(User).filter(User.user_id == user_id).first()
    return user

#updates the groups that user belongs to and the user's first name and last name as well
def user_put(payload):
    user = session.query(User).filter(User.user_id == payload.id).first()
    #if user does not exist
    if user == None:
        return None
    user.first_name = payload.first_name
    user.last_name = payload.last_name
    session.commit()
    #a group must exist before a user can join
    for group_name in payload.groups:
        grp = session.query(Group).filter(Group.name == group_name).first()
        user_and_groups = session.query(UserAndGroup).filter(and_(UserAndGroup.user_id == user.id, UserAndGroup.group_id == grp.id))
        #if there is no relationship between the group and the user add user to the group
        if user_and_groups == None:
            create_user_and_group = UserAndGroup(user_id = user.id, group_id = grp.id)
            session.add(create_user_and_group)
        #if the user is in the group remove the user
        else:
            session.delete(user_and_groups)
        session.commit()
    return user

#creates new user in the database and adds users to groups
def user_post(payload):
    #check if a user with the user id already exists
    user_ = session.query(User).filter(User.user_id == payload.id).first()
    if user_ != None:
        return None
    #create a new user
    user_ = User(id = payload.id, first_name = payload.first_name, last_name=payload.last_name)
    session.add(user_)
    session.commit()

    user_ = session.query(User).filter(User.user_id == payload.id).first()
    #groups must exist before a user can join to the group
    for group in payload.groups:
        grp = session.query(Group).filter(Group.name == group).first()
        #Add an entry to groups_users table
        user_and_group = UserAndGroup(user_id = user_.id, group_id = grp.id)
        session.add(user_and_group)
        session.commit()
    return user_

def group_delete():
    pass

def group_get():
    pass

def group_post():
    pass

def group_put():
    pass

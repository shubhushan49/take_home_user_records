from os import name
from database_helper import session, User, Group, UserAndGroup
from sqlalchemy.sql.expression import and_, update
import json
#response object for user endpoint
def response_user(data):
    return json.dumps(data)

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
#deletes the group and the relationship between members and the group
def group_delete(grp_name):
    group = session.query(Group).filter(Group.name == grp_name).first()
    if group == None:
        return None
    #fetch all records for the group
    users_and_group = session.query(UserAndGroup).filter(UserAndGroup.group_id == group.id)
    #delete all records of the group
    for relationship in users_and_group:
        session.delete(relationship)
        session.commit()
    #delete the group
    session.delete(group)
    session.commit()
    return "Success"
#fetches all members of the group
def group_get(grp_name):
    #fetch details of the group
    group = session.query(Group).filter(Group.name == grp_name).first()
    if group == None:
        return None
    #get the relationship between users table and group table
    users_and_groups = session.query(UserAndGroup).filter(UserAndGroup.group_id == group.id)
    if users_and_groups == None:
        return None
    members_list = []
    for row in users_and_groups:
        #fetch users of the group from the user table
        user = session.query(User).filter(User.id == row.user_id).first()
        members_list.append(user.user_id)
    return members_list

#creates a new group if a group with the same name does not exist in the database
def group_post(grp_name):
    group = session.query(Group).filter(Group.name == grp_name).first()
    if group!=None:
        return None
    new_grp = Group(name=grp_name)
    session.add(new_grp)
    session.commit()
    return []
#kicks out users if they are in the group, adds them if they are not a member of the group
def group_put(grp_name, members_list):
    group = session.query(Group).filter(Group.name == grp_name).first()
    #the group does not exist
    if group == None:
        return None
    for member in members_list:
        user = session.query(User).filter(User.user_id == member)
        #if a user does not exist
        if user == None:
            return None
        #if the user is present in the group remove member from the relationship table
        user_in_group = session.query(UserAndGroup).filter(and_(UserAndGroup.group_id == group.id, UserAndGroup.user_id == user.id)).first()
        if user_in_group != None:
            session.delete(user_in_group)
        else:
            #if the user is not in the group, add to the relationship table
            add_user_to_group = UserAndGroup(user_id = user.id, group_id = group.id)
            session.add(add_user_to_group)
        session.commit()
    
    updated_member_list = []
    #fetch the updated records of the group
    mem_list = session.Query(UserAndGroup).filter(UserAndGroup.group_id == group.id)
    for mem in mem_list:
        user = session.Query(User).filter(User.id == mem.user_id)
        updated_member_list.append(user.user_id)
    return updated_member_list

from database_helper import *
def populate_database():
    #id = 1
    session.add(User(user_id="johnny123", first_name="John", last_name="Don"))
    #id = 2
    session.add(User(user_id="luffy", first_name="Monkey", last_name="Luffy"))
    #id = 3
    session.add(User(user_id="zoro", first_name="Roronoa", last_name="Zoro"))
    #id = 4
    session.add(User(user_id="sanji", first_name="vinsmoke", last_name="Sanji"))
    #id = 5
    session.add(User(user_id="robin", first_name="Nico", last_name="Robin"))
    #id = 6
    session.add(User(user_id="nami", first_name="Nami", last_name=""))
    #id = 7
    session.add(User(user_id="dragon", first_name="Monkey", last_name="Dragon"))
    #id = 8
    session.add(User(user_id="garp", first_name="Monkey", last_name="Garp"))
    #id = 9
    session.add(User(user_id="sabo", first_name="Monkey", last_name="Sabo"))
    #id = 10
    session.add(User(user_id="ace", first_name="Portgas", last_name="Ace"))
    session.commit()

    #id = 1
    session.add(Group(name="mugiwara"))
    #id = 2
    session.add(Group(name="navy"))
    #id = 3
    session.add(Group(name="revolutionary"))
    #id = 4
    session.add(Group(name="unknown"))
    session.commit()


    session.add(UserAndGroup(user_id=1, group_id=4))
    session.add(UserAndGroup(user_id=2, group_id=1))
    session.add(UserAndGroup(user_id=3, group_id=1))
    session.add(UserAndGroup(user_id=4, group_id=1))
    session.add(UserAndGroup(user_id=5, group_id=1))
    session.add(UserAndGroup(user_id=6, group_id=1))
    session.add(UserAndGroup(user_id=8, group_id=2))
    session.add(UserAndGroup(user_id=7, group_id=3))
    session.add(UserAndGroup(user_id=9, group_id=3))
    session.add(UserAndGroup(user_id=10, group_id=2))
    session.add(UserAndGroup(user_id=10, group_id=1))
    session.add(UserAndGroup(user_id=1, group_id=2))
    session.add(UserAndGroup(user_id=2, group_id=2))
    session.add(UserAndGroup(user_id=3, group_id=4))
    session.add(UserAndGroup(user_id=4, group_id=4))
    session.commit()

if __name__ == "__main__":
    populate_database()
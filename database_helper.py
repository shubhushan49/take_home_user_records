from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import and_, table
import sys
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    first_name = Column(String(50))
    last_name = Column(String(50))

    children = relationship("UserAndGroup")

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    children = relationship("UserAndGroup")

class UserAndGroup(Base):
    __tablename__ = "groups_users"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True)

def drop_all_tables():
    eng = create_engine("postgresql://admin:admin@localhost:5432/take_home_test", echo=False)
    eng.execute("DROP TABLE users, groups, groups_users")

if __name__ == "__main__":
    DATABASE_PROD = "take_home_production"
    DATABASE_TEST = "take_home_test"
    db = None

    #checks if we are in production mode or just testing
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        db = DATABASE_TEST
    else:
        db = DATABASE_PROD

    engine = create_engine(f"postgresql://admin:admin@localhost:5432/{db}", echo=False)
    Session = sessionmaker(bind = engine)
    session = Session()
    Base.metadata.create_all(engine)
else:
    engine = create_engine("postgresql://admin:admin@localhost:5432/take_home_test", echo=False)
    Session = sessionmaker(bind = engine)
    session=Session()
    
"""
Learning SQL Alchemy

#creates all tables
Base.metadata.create_all(engine)


#Inserting data to the database
#create an instance of the model
user = User(id="shubhushan", first_name="shubhushan", last_name="kattel")
#stage data to the current session
session.add(user)
#commit data to the database
session.commit()

if we have multiple users: user1, user2, user3....usern
then: session.add_all([user1, user2,...usern])
session.commit()


#Query data from the database
#get all data from users table
users = session.query(User)

for user_ in users:
    print(user_.first_name, user_.last_name, user_.id)
#order by
users = session.query(User).order_by(User.first_name)

#filtering
user_ = session.query(User).filter(User.first_name=="firstname")
user_ = session.query(User).filter(and_(User.first_name=="firstname", User.last_name=="last_name", User.id=="id")).first()


#updating data in the database
user_ = session.query(User).filter(User.first_name=="shubhushan").first()
user_.name = "shambhu"
session.commit()


#deleting data in the database
user_ = session.query(User).filter(User.first_name=="shambhu").first()
session.delete(user_)
session.commit()
"""
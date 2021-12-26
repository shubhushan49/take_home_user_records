import json
import unittest

from sqlalchemy.sql import base
from database_helper import *
from helper_functions import validate_user_record
import requests

class TestEndpoints(unittest.TestCase):
    base_url = "http://localhost:5000"
    user_url = base_url+"/users"
    group_url = base_url+"/groups/"

    def test_get_users_exists(self):
        r = requests.get(self.user_url+"?user_id=luffy")
        data = r.json()
        self.assertEqual(True, validate_user_record(data['data']))
    
    def test_get_users_dont_exist(self):
        r = requests.get(self.user_url+"?useri_id=naruto")
        data = r.status_code
        self.assertEqual(404, data)
    
    def test_get_users_parameter_not_defined(self):
        r = requests.get(self.user_url)
        data = r.status_code
        self.assertEqual(404, data)
    
    def test_post_user_already_exists(self):
        user_data = {"id": "luffy", "first_name":"xxx", "last_name": "xxx", "groups": "xxx"}
        r = requests.post(self.user_url, data=json.dumps(user_data), headers={"Content-Type":"application/json"})
        data = r.status_code
        self.assertEqual(409, data)
    
    def test_post_user_invalid_json(self):
        user_data = {"id": "haha", "first_name": "xxx", "last_name": "xxx",}
        r = requests.post(self.user_url, data=json.dumps(user_data), headers={"Content-Type":"application/json"})
        data = r.status_code
        self.assertEqual(400, data)
    
    def test_post_user(self):
        user_data = {"id": "aokiji", "first_name": "????", "last_name": "xxx", "groups": ["navy"]}
        r = requests.post(self.user_url, data=json.dumps(user_data), headers={"Content-Type":"application/json"})
        data = r.json()
        self.assertEqual(True, validate_user_record(data['data']))
    
    def test_put_user(self):
        user_data = {"id": "aokiji", "first_name": "aokiji", "last_name": "???", "groups": ["mugiwara"]}
        r = requests.put(self.user_url, data = json.dumps(user_data), headers={"Content-Type":"application/json"})
        data = r.json()
        self.assertEqual(True, validate_user_record(data['data']))

    def test_put_user_dont_exist(self):
        user_data = {"id": "ivankov", "first_name": ">>>", "last_name": "....", "groups": ["navy"]}
        r = requests.put(self.user_url, data=json.dumps(user_data), headers={"Content-Type": "application/json"})
        data = r.status_code
        self.assertEqual(404, data)

    def test_put_user_inavlid_json(self):
        user_data = {"id": "xxx", "first_name": "xxx"}
        r = requests.put(self.user_url, data = json.dumps(user_data), headers={"Content-Type": "application/json"})
        data = r.status_code
        self.assertEqual(409, data)

if __name__ == "__main__":
    unittest.main()
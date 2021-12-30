import json
import unittest

from sqlalchemy.sql import base
from database_helper import *
from helper_functions import validate_user_record
import requests

class TestEndpoints(unittest.TestCase):
    base_url = "http://localhost:5000"
    user_url = base_url+"/users"
    group_url = base_url+"/groups"

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

    def test_delete_user_not_in_database(self):
        user_data = {"id": "hahaha"}
        r = requests.delete(self.user_url, data= json.dumps(user_data), headers={"Content-Type": "application/json"})
        data = r.status_code
        self.assertEqual(404, data)
    
    def test_delete_user_id_not_provided(self):
        user_data = {"first_name" : "hola"}
        r = requests.delete(self.user_url, data = json.dumps(user_data), headers={"Content-Type": "application/json"})
        data = r.status_code
        self.assertEqual(409, data)
    
    def test_delete_user(self):
        user_data = {"id": "garp"}
        r = requests.delete(self.user_url, data = json.dumps(user_data), headers={"Content-Type": "application/json"})
        data = r.status_code
        self.assertEqual(204, data)

    def test_get_group(self):
        group_name = "mugiwara"
        r = requests.get(self.group_url+f"/{group_name}")
        data = r.json()
        #if users are returned then assert true
        if data.get("users") != None:
            self.assertTrue(True)
        else:
            self.assertFalse(True)
    
    def test_get_group_does_not_exist(self):
        group_name = "naruto"
        r = requests.get(self.group_url+f"/{group_name}")
        data = r.status_code
        self.assertEqual(404, data)
    
    def test_post_group(self):
        group_name = "bleach"
        r = requests.post(self.group_url+f"/{group_name}")
        data = r.json()

        if data.get("users") != None:
            self.assertTrue(True)
        else:
            self.assertFalse(True)
    
    def test_post_group_already_exists(self):
        group_name = "navy"
        r = requests.post(self.group_url+f"/{group_name}")
        data = r.status_code
        self.assertEqual(409, data)
    
    def test_put_group_does_not_exist(self):
        group_name = "hunterxhunter"
        data = {
            "users": ["luffy", "sanji", "zoro"]
        }
        r = requests.put(self.group_url+f"/{group_name}", data = json.dumps(data), headers={"Content-Type": "application/json"})
        data = r.status_code
        self.assertEqual(409, data)
    
    def test_put_group(self):
        group_name = "mugiwara"
        data = {
            "users": ["luffy", "sanji", "zoro"]
        }
        r = requests.put(self.group_url+f"/{group_name}", data = json.dumps(data), headers={"Content-Type": "application/json"})
        data = r.json()

        if data.get("users") != None:
            self.assertTrue(True)
        else:
            self.assertFalse(True)
    
    def test_delete_group_does_not_exist(self):
        group_name = "hunterxhunter"
        r = requests.delete(self.group_url+f"/{group_name}")
        data = r.status_code
        self.assertEqual(404, data)
    
    def test_delete_group(self):
        group_name = "unknown"
        r = requests.delete(self.group_url+f"/{group_name}")
        data = r.status_code
        self.assertEqual(204, data)

if __name__ == "__main__":
    unittest.main()
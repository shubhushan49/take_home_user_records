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
    def test_get_users(self):
        r = requests.get(self.user_url+"?user_id=luffy")
        data = r.json()
        self.assertEqual(True, validate_user_record(data['data']))

if __name__ == "__main__":
    unittest.main()
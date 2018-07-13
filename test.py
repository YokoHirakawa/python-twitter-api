from helpers import app
from unittest import TestCase
import unittest
import json

class TestIntegrations(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_users(self):
        response = self.app.get('/users/ElonMusk')
        print(repr(response.data))

        assert(response.status_code==200) # OK
        assert(response.data!="") # data not blank

        # https://stackoverflow.com/questions/38256810/how-to-create-a-unit-test-to-check-the-response-of-an-api-made-in-flask
        jsonstr = response.get_data(as_text=True) 
        data = json.loads(jsonstr) # decode data from json to python
        print(len(data))
        assert(len(data) > 0) # check we got tweets

    def test_hashtags(self):
        response = self.app.get('/hashtags/SpaceX')
        #print(repr(response.data))
        assert(response.status_code==200)
        assert(response.data!="")

        jsonstr = response.get_data(as_text=True)
        data = json.loads(jsonstr)
        print(len(data))
        assert(len(data) > 0)

if __name__ == "__main__":
    unittest.main()

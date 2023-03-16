import os
import unittest
import json
from pymongo import MongoClient
from flask import session


from app import create_app
from db.models import UserRepo, TaskRepo, User, Task

class AppTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.client = self.app.test_client
        self. Client = MongoClient('mongodb://localhost:27017/')
        self.db = self.Client['dbTest']
        self.Tasks = self.db["Tasks"]
        self.Users = self.db["Users"]
        
        return super().setUp()
    
    def  tearDown(self) -> None:
        return super().tearDown()
    
    def test_get_login_page(self):
        res = self.client().get('/')
        
        self.assertEqual(res.status_code, 200)
        
    def user_sign_up_success(self):
        dtls = {
            "firstName" : "Isaiah",
            "surnmae" : "Faluyi",
            "email" : "faluyi@gmail.com",
            "pswd" : "faluyi"
        }
        
        res = self.client().post('/User/Sign_up', json=dtls)
        
        self.assertEqual(res.status_code, 302)

    
    def test_logout(self):
        res = self.client().get('/logout_user')
        
        self.assertEqual(res.status_code, 302)
        
    def redirect_access_to_homepage_if_not_login(self):
        
        res = self.client().get('/home')
        data = res.data
                
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["tasks"])
        self.assertTrue(len(data["tasks"]))
        
    def test_user_login_success(self):
        res = self.client().post('/login/authenticateUser', json={"email": "phirmzhy@gmail.com", "pswd": "akindele"})
        
        self.assertEqual(res.status_code, 302)
        
    


if __name__ == "__main__":
    unittest.main()
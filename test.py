import os
import unittest
import json
from pymongo import MongoClient
#from flask import session


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
        
    def test_user_sign_up_success(self):
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
        
    def test_access_to_homepage_redirect_if_not_login(self):
        
        res = self.client().get('/home')
                
        self.assertEqual(res.status_code, 302)
        
    def test_user_login_success(self):
        
        res = self.client().post('/login/authenticateUser', json={"email": "faluyi@gmail.com", "pswd": "faluyi"})
        
        self.assertEqual(res.status_code, 302)
        
    def test_get_create_task_form(self):
        res = self.client().get('/task/create')
        
        self.assertEqual(res.status_code, 200)
        
    def test_post_create_task_form_success(self):
        user = UserRepo().get_one_user()
        dtls = {
            "user_id" : user["_id"],
            "id" : "html001",
            "name" : "into to html",
            "deadline" : "10-04-2021",
            "progress" : "in progress",
            "description" : "create a simple html file"
        }
        
        res = self.client().post('/task/create', json=dtls)
        
        self.assertEqual(res.status_code, 302)
        
    #def test_post_create_task_form_failed(self):
       # user = list(self.Users.find_one())
      #  dtls = {
       #     "user_id" : user._id,
        #    "id" : "html001",
         #   "name" : "into to html",
          #  "deadline" : "10-04-2021",
           # "progress" : "in progress",
            #"description" : "create a simple html file"
        #}
        
       # res = self.client().post('/task/create', json=dtls)
        
        #self.assertEqual(res.status_code, 200)
        
    def test_view_task(self):
        task = list(self.Tasks.find_one())
        dtls = {
            "task_id" : task.id,
        }
        res = self.client().post('/task/view_task', json=dtls)
        self.assertEqual(res.status_code, 200)
        
    def test_update_task_progress_(self):
        task = list(self.Tasks.find_one())
        dtls = {
            "task_id" : task.id,
            "progress" : task.progress
        }
        res = self.client().get('/task/update_progress', json=dtls)
    
    def test_sort_task_by_status(self):
        pass
    
    def test_sort_task_by_due_date(self):
        pass
    


if __name__ == "__main__":
    unittest.main()
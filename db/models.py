from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
Tasks = db["Tasks"]
Users = db["Users"]

class UserRepo:
    def __init__(self) -> None:
        self.collection = db['Users']
        
    def get_all_users(self):
        return self.collection.find()

    def create_user(self, user):
        return self.collection.insert_one(user.__dict__)

    def get_user_by_email(self, email):
        return self.collection.find_one({"email": email})

    def get_user_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def update_user(self, id, **kwargs):
        return self.collection.update_one(
           {"_id": ObjectId(id)}, {"$Set": kwargs}).modified_count > 0


class TaskRepo:
    def __init__(self) -> None:
        self.collection = db['Tasks']

    def get_all_tasks(self):
        return self.collection.find()
    
    def create_task(self, task):
        return self.collection.insert_one(task.__dict__)
    
    def get_task_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def get_task_by_task_id(self, task_id):
        return self.collection.find_one({"id": task_id})

    def update_task(self, task_id, progress):
        task = self.get_task_by_task_id(task_id)
        prg = task["progress"]
        if prg==progress:
            return "the same"
        else:
            return self.collection.update_one(
           {"id": task_id}, {"$set": {"progress":progress}}).modified_count > 0

     
class User:
    def __init__(self, firstName, surname, email, pswd) -> None:
        self.email = email
        self.firstname = firstName
        self.surname = surname
        self.password = pswd
        
class Task:
    def __init__(self, id, name, assigned_to, date_assigned, deadline, progress, description) -> None:
        self.id = id
        self.name = name
        self.assigned_to = assigned_to
        self.date_assigned = date_assigned
        self.deadline = deadline
        self.progress = progress
        self.description = description
        
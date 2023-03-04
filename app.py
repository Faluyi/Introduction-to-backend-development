from pymongo import MongoClient

from flask import Flask, render_template, request, redirect, url_for, session, flash
import datetime
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
Tasks = db["Tasks"]
Users = db["Users"]



app = Flask(__name__)
app.secret_key= "faluyi"

    

@app.route('/')
def index():
   return render_template('forms/login.html')

@app.route('/User/Sign_up', methods=["POST"])
def createUser():
    user = {
        "firstName" : request.form.get('first_name'),
        "surname" : request.form.get('surname'),
        "_id" : request.form.get('email'),
        "pswd" : request.form.get('pswd'),
        "tasks" : {}
        }
    Users.insert_one(user)
    return redirect(url_for('index'))


@app.route('/login/authenticateUser', methods=["POST"])
def authenticateUser():
    id = request.form.get('email')
    pswd = request.form.get('pswd')
    query = {"_id": id}
    usr = Users.find(query)
    
    try:
        if usr:
            app.logger.info(usr)
            for user in usr:
                if user["pswd"]==pswd:
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('index'))
                    flash ("Invalid Login details")
    except TypeError:
        return redirect(url_for('index'))
        flash('Invalid Login details')

@app.route('/home')
def home():
    tasks=[]
    for x in Tasks.find():
        tasks.append(x)
        
    return render_template('pages/home.html', tasks=tasks)
    
    
@app.route('/task/create', methods = ["POST", "GET"])
def create_task():
    if request.method == "POST":
        user_id = request.form.get("user")
        task = {
        "_id" : request.form.get('Task_id'),
            "name" : request.form.get('Task_title'),
            "assigned_to" :user_id,
            "date_assigned": datetime.datetime.now(),
           "deadline" : request.form.get("Deadline"),
           "progress": request.form.get("progress"),
           "description": request.form.get("description")
            }   

        id = Tasks.insert_one(task)
        
        query = {"_id": user_id}
        #tasks = []
        #for user in Users.find(query):
            #tasks.append(user.tasks)
            
        
        new={'$set':{"tasks":task}}
        Users.update_one(query,new)
        
        if id :
            flash ("Task successfully created")
            return redirect(url_for("home"))
        else:
            flash ("Invalid details ")
    else:
        users = Users.find()
        return render_template('forms/create_task.html',users=users)



@app.route('/task/view_task', methods=["POST","GET"])
def view_task():
    task_id = request.form.get('task_id')
    query = {"_id": task_id}
    app.logger.info(query)
    data = []
    for x in Tasks.find(query):
        data.append(x)
    app.logger.info(data)
    return render_template('/pages/view_task.html', task_id=task_id, data=data)
    

@app.route('/task/update_progress', methods=["POST","GET"])
def update_progress():
    task_id = request.args.get("Task_id")
    progress = request.args.get("progress")
    query={"_id":task_id} 
    new={'$set':{"progress":progress}}
    Tasks.update_one(query,new)

    return redirect(url_for("home"))
        
# Using this as a test comment

if __name__ =="__main__":
    app.run(debug=True)

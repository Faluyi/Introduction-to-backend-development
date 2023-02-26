from pymongo import MongoClient

from flask import Flask, render_template, request, redirect, url_for, session, flash
import datetime
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
Tasks = db["Tasks"]
task_breakdown =  db["task_breakdown"]


app = Flask(__name__)
app.secret_key= "faluyi"

#@app.route('/')
#def index():
 #   return render_template('forms/login.html')

@app.route('/')
def index():
    tasks=[]
    for x in Tasks.find():
        tasks.append(x)
        
    return render_template('pages/home.html', tasks=tasks)
    
    
@app.route('/task/create', methods = ["POST", "GET"])
def create_task():
    if request.method == "POST":
        task = {
        "_id" : request.form.get('Task_id'),
            "name" : request.form.get('Task_title'),
            "assigned_to" : request.form.get("asigned_to"),
            "date_assigned": datetime.datetime.now(),
           "deadline" : request.form.get("Deadline"),
           "progress": request.form.get("progress"),
           "description": request.form.get("description")
            }   

        Tasks.insert_one(task)
        return redirect(url_for("index"))
    else:
        return render_template('forms/create_task.html')
    
    
#@app.route('/task/add_breakdown',methods= ["POST","GET"] )
#def add_breakdown():
 #   task_id = request.form.get('task_id')
  #  if request.method=="POST":
   #     data ={"Task_id": task_id,
    #       "breakdown":request.form.get('breakdown') ,
     #      "progress": ""
       #   }
      #  task_breakdown.insert_one(data)
    
        
    #return redirect(url_for('load_breakdown', data=data, task_id=task_id))

    
    
#@app.route('/task/breakdown', methods = ["POST","GET"])
#def load_breakdown():
  #  data=[]
  #  breakdown=[]
  #      data.append(x)
   # for y in task_breakdown.find():
    #    breakdown.append(y)
    #return render_template('forms/add_breakdown.html', data=data, breakdown=breakdown)



@app.route('/task/view_task', methods=["POST","GET"])
def view_task():
        task_id = request.form.get('task_id')
        query = {"_id": task_id}
        data = []
        for x in Tasks.find(query):
            data.append(x)
        return render_template('/pages/view_task.html', task_id=task_id, data=data)


@app.route('/task/update_progress/', methods=["POST"])
def update_progress(): 
    if request.method == "GET" :
        query = task_breakdown.find()
        for param in query["_id"]:
            progress=request.args.get(param,"")
            query={"_id":param} 
            new={'$set':{"progress":progress}}
            task_breakdown.update_one(query,new)

    return redirect(url_for("index"))
    
        
# Using this as a test comment

if __name__ =="__main__":
    app.run(debug=True)

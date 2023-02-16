from pymongo import MongoClient

from flask import Flask, render_template, request, redirect, url_for,session,flash
import datetime
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
Tasks = db["Tasks"]
task_breakdown =  db["task_breakdown"]


app = Flask(__name__)
app.secret_key= "faluyi"

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
           "deadline" : request.form.get("Deadline")
            }   

        Tasks.insert_one(task)
        return redirect(url_for("index"))
    else:
        return render_template('forms/create_task.html')
    
    
@app.route('/task/add_breakdown',methods= ["POST","GET"] )
def add_breakdown():
    task_id = request.form.get('task_id')
    if request.method=="POST":
        data ={"Task_id": task_id,
           "breakdown":request.form.get('breakdown') ,
           "progress":" "
          }
        task_breakdown.insert_one(data)
    
        
    return redirect(url_for('load_breakdown', data=data, task_id=task_id))

    
    
@app.route('/task/breakdown', methods = ["POST","GET"])
def load_breakdown():
    data=[]
    breakdown=[]
    for x in Tasks.find():
        data.append(x)
    for y in task_breakdown.find():
        breakdown.append(y)
    return render_template('forms/add_breakdown.html', data=data, breakdown=breakdown)



@app.route('/task/view_progress', methods=["POST"])
def view_progress():
    task_id = request.form.get('task_id')
    data=[]
    prg=[]
    for x in task_breakdown.find({"Task_id":task_id}):
        data.append(x)
        if x["progress"]=="on":
            prg.append({"progress":"checked"})
    return render_template('/pages/task_progress.html', data=data, task_id=task_id,prg=prg)


@app.route('/task/update_progress', methods=["POST","GET"])
def update_progress():
    if request.method=="POST":
                
        for brk in task_breakdown.find():
            for dt in range(len(brk)):
                progress=request.form.get(brk[dt])
                query={"Task_id":(brk[dt])["Task_id"]}
                new={"$set":{"progress":progress}}
                task_breakdown.update_one(query,new)
            
        return redirect(url_for("index"))
        


if __name__ =="__main__":
    app.run(debug=True)
 
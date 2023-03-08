from db.models import User,Task,UserRepo,TaskRepo
from flask import Flask, render_template, request, redirect, url_for, session, flash
import datetime



app = Flask(__name__)
app.secret_key= "faluyi"

user_repo = UserRepo()
task_repo = TaskRepo()
    
#returns the login page
@app.get('/')
def index():
    if "user" in session:
        return redirect(url_for('home'))
    else:
        return render_template('forms/login.html')

#get user details and create user
@app.post('/User/Sign_up')
def createUser():
        firstName = request.form.get('first_name')
        surname = request.form.get('surname')
        email =  request.form.get('email')
        pswd = request.form.get('pswd')
        usr = user_repo.get_user_by_email(email)
        if usr:
            flash('an account is already attached to the email address inputed')
            return redirect(url_for('index'))
        else:
            user = User(firstName, surname, email, pswd)
            created = user_repo.create_user(user)
            if created:
                flash('Sign up successful')
                return redirect(url_for('index'))
            else:
                flash('Sign up not successfull')
                return redirect(url_for('index'))


@app.post('/login/authenticateUser')
def authenticateUser():
    email = request.form.get('email')
    pswd = request.form.get('pswd')
    user = user_repo.get_user_by_email(email)
    
    if user:
        app.logger.info(user)
        if user["password"]==pswd:
            session["user"] = email
            flash('Welcome!' + " " + user["surname"] + " " + user["firstname"])
            return redirect(url_for('home'))
        else:
            flash("Login attempt failed! Incorrect password")
            return redirect(url_for('index'))
    else:
        flash("Login attempt failed! Invalid Login details")
        return redirect(url_for('index'))

@app.get('/logout_user')
def logout():
    session.pop("user",None)
    return redirect(url_for('index'))    

@app.get('/home')
def home():
    if "user" in session:
        tasks=[]
        for x in task_repo.get_all_tasks():
            tasks.append(x)
        return render_template('pages/home.html', tasks=tasks)
    else:
        flash(" Ooops,You aren't logged in! Log in and try again")
        return redirect(url_for('index'))
    
    
@app.route('/task/create', methods=["POST","GET"])
def create_task():
    if "user" in session:
        if request.method == "POST":
            user_id = request.form.get("user")
            user = user_repo.get_user_by_id(user_id)
            users = user_repo.get_all_users()

            full_name = "{0} {1}".format(user["firstname"], user["surname"])
            
            id = request.form.get('Task_id')
            name = request.form.get('Task_title')
            assigned_to = {"user_id": user_id, "full_name": full_name}
            date_assigned = datetime.datetime.now()
            deadline = request.form.get("Deadline")
            progress = request.form.get("progress")
            description = request.form.get("description")  
            
            check_id = task_repo.get_task_by_task_id(id)
            
            if check_id:
                flash('Task creation failed!, try using another task id')
                return render_template('/forms/create_task.html', users=users)
            else:
                task = Task(id, name, assigned_to, date_assigned, deadline, progress, description)
                created = task_repo.create_task(task)
                
                if created:
                    flash (id + " successfully created")
                    return redirect(url_for("home"))
                else:
                    flash ("Invalid details ")
                    return render_template('/forms/create_task.html', users=users)
        else:
            users = user_repo.get_all_users()
            return render_template('/forms/create_task.html', users=users)
    else:
        flash(" Ooops,You aren't logged in! Log in and try again")
        return redirect(url_for('index'))


@app.post('/task/view_task')
def view_task():
    if "user" in session:
        task_id = request.form.get('task_id')
        data = task_repo.get_task_by_task_id(task_id)
        app.logger.info(data)
        return render_template('/pages/view_task.html', task_id=task_id, data=data)
    else:
        flash(" Ooops,You aren't logged in! Log in and try again")
        return redirect(url_for('index'))
    

@app.get('/task/update_progress')
def update_progress():
    if "user" in session:
        task_id = request.args.get("Task_id")
        progress = request.args.get("progress")
        status = task_repo.update_task(task_id, progress)

        if status == "the same":
            flash('No update made')
            return redirect(url_for("home"))
        elif status == True:
            flash(task_id + ' updated successfully!')
            return redirect(url_for("home"))
        else:
            flash('Update not successful')
            return redirect(url_for("home"))
    else:
        flash(" Ooops,You aren't logged in! Log in and try again")
        return redirect(url_for('index'))


if __name__ =="__main__":
    app.run(debug=True)


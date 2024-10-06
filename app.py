from flask import Flask , render_template ,url_for , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#database confirguration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'   # triple slash is used for relative path  and four is for absolute path
app.config['SECRET_KEY'] = 'SUPER_SECRET_KEY'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# model 
class Todo(db.Model):
  id  = db.Column(db.Integer , primary_key =True) # these are column of the model todo of our database , it contains unique id , content , date it is created
  content = db.Column(db.String(200) , nullable = False)
  date_created = db.Column(db.DateTime , default = datetime.utcnow)

  def __repr__(self):    # everytime new entry is created this function will run and return id of the task
    return '<Task %r>' % self.id    
 
#routes
@app.route('/',methods=['POST','GET'])  # function will be executed and index.html file will run 
def index(): 
  if request.method == 'POST':  # when new task is being added 
    task_content = request.form['content']   # it will take data from form we created and store it in task_content
    new_task = Todo(content = task_content)  # then it will update our db with the task_content

    try: 
      db.session.add(new_task)  # this will add new task to db 
      db.session.commit()  
      return redirect('/')  # after adding the task it will redirect it to the home page
    
    except:
      return 'there was an issue adding your task'  # if there is an issue it will return this error
    
  else:
    tasks = Todo.query.order_by(Todo.date_created).all()   # this is used to arrange all task in an order according to there date_created 
    # here we can also use first() instead of all() to show latest task created 
    return render_template('index.html' , tasks= tasks)    

# wrting function and route for delete operation 
# for deleting a task we need task unique id

@app.route('/delete/<int:id>') # this will work when delete operation is called 
def delete(id):
  task_to_delete = Todo.query.get_or_404(id)  # this will get the task id and if id is not there will return 404 error

  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
  except: 
    return "there was a problem in performing delete operation"
  
# for update we need to make another route and function
@app.route('/update/<int:id>' , methods=['POST','GET'])
def update(id):
  task_to_update = Todo.query.get_or_404(id)
  if request.method == 'POST':
    task_to_update.content = request.form['content']

    try:
      db.session.commit()
      return redirect('/')

    except:
      return "error encountered while updating the task"

  else:
    return render_template('update.html' , task = task_to_update)

if __name__ == "__main__":
  with app.app_context():
    db.create_all()
    app.run(debug=True)


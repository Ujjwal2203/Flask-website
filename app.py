from flask import Flask , render_template ,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#database confirguration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'   # triple slash is used for relative path  and four is for absolute path
db = SQLAlchemy(app)



# model 
class Todo(db.Model):
  id  = db.Column(db.Integer , primary_key =True) # these are column of the model todo of our database , it contains unique id , content , date it is created
  content = db.Column(db.String(200) , nullable = False)
  date_created = db.Column(db.DateTime , default = datetime.utcnow)

  def __repr__(self):    # everytime new entry is created this function will run and return id of the task
    return '<Task %r>' % self.id    
 
#with app.app_context():
#  db.create_all()
#routes
@app.route('/')  # function will be executed and index.html file will run
def index():
  return render_template('index.html')   

if __name__ == "__main__":
  app.run(debug=True)


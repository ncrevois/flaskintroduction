from flask import Flask , render_template, url_for, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  #referencing this file 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #where our database is located 
db = SQLAlchemy(app)  #our database is being initialized with the settings from our app 

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False) #don't want to let the user create a task with content empty so nullable=False
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

#create an index route so when we browse to the url we don't immediately 404 
@app.route('/', methods = ['POST', 'GET']) #there are 2 methods that this route can accept

def index():
    if request.method == 'POST': #if the request that is send to this route is POST
        task_content = request.form['content']  #input inside the box 
        new_task = Todo(content = task_content)

        try:
            #push to the database 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except: 
            return("There was an issue adding your task.")
    else: 
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks = tasks)  #knows to look into the templates folder 


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)  #get the task from the database, unless the task doesn't exist then 404 

    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except: 
        return('There was a problem deleting your task.')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try: 
            db.session.commit()
            return redirect('/')  #back to homepage 
        except: 
            return 'There was an issue updating your task'
    else: 
        return render_template('update.html', task = task)

if __name__ == '__main__': 
    app.run(debug=True)

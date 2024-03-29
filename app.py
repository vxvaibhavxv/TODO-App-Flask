from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    dateCreated = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        """
        String to be printed when printing the object
        """
        return f"{self.sno} | {self.title}"

def createTodo(title, description):
    myTODO =  Todo(title = title, description = description)
    db.session.add(myTODO)
    db.session.commit()

@app.route("/", methods = ["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form["todoTitle"]
        description = request.form["todoDescription"]
        createTodo(title, description)

    allTodo = Todo.query.all()
    return render_template("index.html", allTodo = allTodo)

@app.route("/todos")
def todos():
    return "<h1>This is products page.</h1>"

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>", methods = ["GET", "POST"])
def update(sno):
    todo = Todo.query.filter_by(sno = sno).first()

    if request.method == "POST":
        todo.title = request.form["todoTitle"]
        todo.description = request.form["todoDescription"]
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    return render_template("update.html", todo = todo)

if __name__ == "__main__":
    app.run(debug = True, port = 8000)
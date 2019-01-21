from flask import Flask,render_template,session,request,redirect,flash
# import the function connectToMySQL from the file mysqlconnection.py
from mysqlconnection import connectToMySQL


app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
DB="usersDB"
@app.route('/users')
def index():
    mysql=connectToMySQL(DB)
    query="SELECT * FROM users"
    users=mysql.query_db(query)

    
    return render_template('index.html',users= users)
@app.route('/users/<int:id>/')
def show(id):
    mysql=connectToMySQL(DB)
    query="SELECT * FROM users WHERE id=%(userid)s"
    data={
        "userid": id
    }
    users=mysql.query_db(query,data)
    return render_template("show.html",users=users[0],id=id)

@app.route('/users/<id>/edit/')
def edit(id):
    mysql=connectToMySQL(DB)
    query="SELECT * FROM users WHERE id=%(userid)s"
    data={
        "userid": id
    }
    users=mysql.query_db(query,data)
    return render_template("edit.html",users=users[0],id=id)


@app.route('/users/<int:id>',methods=["POST"])
def update(id):
    mysql=connectToMySQL(DB)
    query="UPDATE users SET first_name=%(first_name)s,last_name=%(last_name)s,email=%(email)s WHERE id=%(userid)s;"
    data={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "userid":id
    }

    mysql.query_db(query,data)
    return redirect('/users')
@app.route('/users/new')
def new():
    return render_template("new.html")

@app.route('/users/create',methods=["POST"])
def create():
    mysql=connectToMySQL(DB)
    query="INSERT INTO users (first_name,last_name,email) VALUES (%(first_name)s,%(last_name)s,%(email)s);"
    data={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
    }

    mysql.query_db(query,data)
    return redirect('/users')

@app.route('/users/<int:id>/destroy')
def delete(id):
    mysql=connectToMySQL(DB)
    query="DELETE FROM users WHERE id=%(userid)s"
    data={
        "userid":id
    }

    mysql.query_db(query,data)
    return redirect('/users')
if __name__ == "__main__":
    app.run(debug=True)
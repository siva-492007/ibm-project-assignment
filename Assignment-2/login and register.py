from os import stat
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

app = Flask(__name__)
app.secret_key = 'Zenik'

DATABASE = "bludb"
HOSTNAME = "fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
PORT = 32731
UID = "qdp46216"
PWD = "MGhHNGxutNYPFPfE"

connection = ibm_db.connect(
    f"DATABASE={DATABASE};HOSTNAME={HOSTNAME};PORT={PORT};SECURITY=SSL;SSLServerCertificate=DigitCertGlobalRootCA.crt;UID={UID};PWD={PWD}", "", ""
)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home', msg=" ")


@app.route('/dashboard')
def dashboard():
    SQL = "SELECT * FROM USERS WHERE username = ?"
    statement = ibm_db.prepare(connection)    
    ibm_db.bind_param(statement, 1, session['username'])
    ibm_db.execute(statement)  
    account = ibm_db.fetch_assoc(statement)   
    return render_template('dashboard.html', title='Dashboard', account=account)


@app.route('/logout')
def logout():
    session.pop('Loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    global user_id
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password'] 
        SQL = "SELECT * FROM USERS WHERE username =? AND password =?"
        statement = ibm_db.prepare(connection)  
        ibm_db.bind_param(statement, 1, username)
        ibm_db.bind_param(statement, 2, password)
        ibm_db.execute(statement)
        account = ibm_db.fetch_assoc(statement)  
        if account:
            session['Loggedin'] = True
            session['id'] = account['USERNAME']
            session['username'] = account['USERNAME']  
            user_id = account['USERNAME']  
            return redirect('/dashboard')
        else:
            message = "Incorrect login credentials"
            return render_template('login.html', title='Login', message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        roll_number = request.form['roll-number'] 
        SQL = "SELECT * FROM USERS WHERE username = ? or email= ?"
        statement = ibm_db.prepare(connection)    
        ibm_db.bind_param(statement, 1, username)
        ibm_db.bind_param(statement, 2, email)
        ibm_db.execute(statement) 
        account = ibm_db.fetch_assoc(statement)    
        if account:
            message = "Account already exists"
        elif not re.match(r'[A-Za-z0-9]+', username):
            message = "Username should be only alphabets and numbers"
        else:
            SQL = "INSERT INTO USERS VALUES (?,?,?,?)"
            statement = ibm_db.prepare(connection)    
            ibm_db.bind_param(statement, 1, username)
            ibm_db.bind_param(statement, 2, email)
            ibm_db.bind_param(statement, 3, roll_number)
            ibm_db.bind_param(statement, 4, password)
            ibm_db.execute(statement) 
            return redirect('/login')  
        return render_template('register.html', message=message, title="Register")

if __name__ == '__main__':
    app.run(debug=True)

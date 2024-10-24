from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask import Flask 
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

users = {'admin': '123'} # Dummy user data for demonstration


@app.route('/')
def retry():
    return render_template('login.html')

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/userprofile')
def userprofile():
    return render_template('userprofile.html')

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']


        cursor = Mysql.connection.cursor()
        cursor.execute('INSERT INTO USERS (Name, Email, Password, confirm_password) VALUES (%s,%s,%s)',(name,email,password,confirm_password))
        Mysql.connent.commit()
        cursor.close()
    return render_template('signIn.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
            return redirect(url_for('retry'))
    
    return render_template('login.html')


# ------------------DataBase---------------

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask_database'


# Create an instance of SQLAlchemy
Mysql = MySQL(app)




# Create the database tables

if __name__ == "__main__":
    app.run(debug=True)

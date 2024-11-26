from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_mysqldb import MySQL
# import bcrypt

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
users = {'admin': '123'} # Dummy user data for demonstration

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '8549941566'
app.config['MYSQL_DB'] = 'Netflix'
app.secret_key = 'your_secret_key_here'  # Secret key for session management

# Password = b"my_secure_Password"
# confirm_password = b"my_secure_password"

# Generate a salt
# salt = bcrypt.gensalt()

# Hash the password using the salt
# Password = bcrypt.hashpw(Password, salt)
# confirm_password = bcrypt.hashpw(confirm_password, salt)

mysql = MySQL(app)

class RegisterForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired(),Email()])
    Password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def retry():
    return render_template('login.html')

@app.route('/home')
def index():
    return render_template('index.html')

# @app.route('/userprofile')
# userprofile():
#     return render_template('userprofile.html')

@app.route('/register', methods=[ 'GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        Password = form.Password.data
        confirm_password = form.confirm_password.data

        # hashed_password = bcrypt.hash(Password.encode('utf-8'),bcrypt.gensalt())
        
        # store data into database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, Password, confirm_password) VALUES (%s, %s, %s, %s)", (name, email, Password, confirm_password))
        mysql.connect.commit()
        cursor.close()
        return redirect(url_for('login'))
    
    return render_template('Register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        Password = request.form['Password']
        
        if username in users and users[username] == Password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
            return redirect(url_for('retry'))
    
    return render_template('login.html')






# def __init__(self, name, email, Password, confirm_password):
#    self.name = name
#    self.email = email
#    self.Password = Password
#    self.confirm_password = confirm_password

# @app.route('/login', methods = ['GET', 'POST'])
# def new():
#    if request.method == 'POST':
#       if not request.form['name'] or not request.form['email'] or not request.form['Password'] or not request.form['confirm_password']:
#          flash('Please enter all the fields', 'error')
#       else:
#          student = students(request.form['name'], request.form['email'],
#             request.form['Password'], request.form['confirm_password'])
         
#          db.session.add(student)
#          db.session.commit()
#          flash('Record was successfully added')
#          return redirect(url_for('show_all'))
#    return render_template('login.html')

# Create the database tables



# @app.route('/home',methods = ['POST', 'GET'])
# def addrec():
#    if request.method == 'POST':
#       try:
#          name = request.form['name']
#          email = request.form['email']
#          Password = request.form['Password']
#          confirm_password = request.form['confirm_password']
         
#          with sql.connect("database.db") as con:
#             cur = con.cursor()
            
#             cur.execute("INSERT INTO students (name,email,Password,confirm_password) VALUES (?,?,?,?)",(name,email,Password,confirm_password) )
            
#             con.commit()
#             msg = "signup successfully"
#       except:
#          con.rollback()
#          msg = "invalid try again"
      
#       finally:
#          return render_template("login.html",msg = msg)
#          con.close()

# Retrive data from the database
# @app.route('/userprofile')
# def list():
#    con = sql.connect("database.db")
#    con.row_factory = sql.Row
   
#    cur = con.cursor()
#    cur.execute("select * from users")
   
#    rows = cur.fetchall();
#    return render_template("list.html",rows = rows)


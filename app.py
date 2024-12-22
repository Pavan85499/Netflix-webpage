from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_mysqldb import MySQL
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


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


mysql = MySQL(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class RegisterForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired(),Email()])
    Password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",validators=[DataRequired()])
    submit = SubmitField("Submit")




@app.route('/register', methods=[ 'GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        Password = form.Password.data
        confirm_password = form.confirm_password.data  
        # store data into database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, Password, confirm_password) VALUES (%s, %s, %s, %s)", (name, email, Password, confirm_password))
        mysql.connect.commit()
        cursor.close()
        return redirect(url_for('login'))   
    return render_template('Register.html', form=form)

# User class for login_manager
class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email
@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
    user_data = cursor.fetchone()
    if user_data:
        return User(id=user_data[0], email=user_data[1])
    return None

# Define SignIn form using WTForms
class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

# Route to display login form and handle login logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Query the database to check user credentials
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", [email])
        user_data = cursor.fetchone()

        if user_data and user_data[2] == password:  # Assuming password is stored as plain text (not secure)
            user = User(id=user_data[0], email=user_data[1])
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html', form=form)



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=100)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])

    # Custom validation for username
    def validate_username(self, field):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (field.data,))
        user = cur.fetchone()
        cur.close()
        if not user:
            raise ValidationError('Username does not exist.')











@app.route('/')
def retry():
    return render_template('login.html')

@app.route('/home')
def index():
    return render_template('index.html')

# @app.route('/userprofile')
# userprofile():
#     return render_template('userprofile.html')

# @app.route('/register', methods=[ 'GET','POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         email = form.email.data
#         Password = form.Password.data
#         confirm_password = form.confirm_password.data

#         # hashed_password = bcrypt.hash(Password.encode('utf-8'),bcrypt.gensalt())
        
#         # store data into database
#         cursor = mysql.connection.cursor()
#         cursor.execute("INSERT INTO users (name, email, Password, confirm_password) VALUES (%s, %s, %s, %s)", (name, email, Password, confirm_password))
#         mysql.connect.commit()
#         cursor.close()
#         return redirect(url_for('login'))
    
#     return render_template('Register.html', form=form)





























































































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

@app.route('/signup', methods=['POST'])
def add_user(): 
   data = request.get_json()
   username = data['username'] 
   email = data['email'] 
   Password = data['Password']  # Define the Password variable
   confirm_password = data['confirm_password']
   cur = mysql.connection.cursor() 
   cur.execute("INSERT INTO users (id, username, email, Password, confirm_password) VALUES (%s, %s, %s, %s, %s)", (id,username, email, Password, confirm_password))
   mysql.connection.commit() 
   cur.close() 
   return jsonify({"message": "User added successfully!"})

if __name__ == "__main__":
    app.run(debug=True)

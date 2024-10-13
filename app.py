from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

users = {'admin': '123'} # Dummy user data for demonstration


@app.route('/login')
def retry():
    return render_template('login.html')

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/userprofile')
def userprofile():
    return render_template('userprofile.html')

@app.route('/signup')
def signup():
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


@app.route('/logout')
def logout():
    # Remove the user from the session (log out)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(debug=True)

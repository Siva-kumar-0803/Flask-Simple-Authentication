from flask import Flask, render_template, request, redirect, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_session import Session

app = Flask(__name__)
mysql = MySQL(app)
bcrypt = Bcrypt(app)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'Replace with your secret key'  
Session(app)

# MySQL configuration
app.config['MYSQL_HOST'] = 'Give Your Host Name'
app.config['MYSQL_USER'] = 'User Name'
app.config['MYSQL_PASSWORD'] = 'Password'
app.config['MYSQL_DB'] = 'Database Name'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Decode to store as string
        cur = mysql.connection.cursor()

        # Check if email already exists
        cur.execute('SELECT email FROM user WHERE email = %s', [email])
        db_email_data = cur.fetchall()

        if db_email_data:
            return "Email already exists"
        else:
            # Insert new user data
            cur.execute('INSERT INTO user (u_name, email, password) VALUES (%s, %s, %s)', (name, email, hashed_password))
            mysql.connection.commit()

        cur.close()
        return redirect('/login')  # Redirect to login after successful registration

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()

        cur.execute('SELECT email, password FROM user WHERE email = %s', [email])
        fetching_email_password = cur.fetchone()
        
        if fetching_email_password:
            hashed_password = fetching_email_password[1]
            if bcrypt.check_password_hash(hashed_password, password):
                # Store the user's email in session to keep them logged in
                session['email'] = email
                return redirect('/home')  # Redirect to the home page on successful login
            else:
                return "Incorrect password"
        else:
            return "Email does not exist"

        cur.close()

    return render_template('login.html')


@app.route('/home')
def home():
    # Check if user is logged in by verifying session
    if not session.get('email'):
        return redirect('/login')  # Redirect to login if not logged in

    return render_template('home.html')  # Render the home page if logged in


@app.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    return redirect('/login')  # Redirect to login after logout


if __name__ == '__main__':
    app.run(debug=True)

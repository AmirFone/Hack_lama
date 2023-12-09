from flask import Flask, request, redirect, url_for,render_template

app = Flask(__name__)

# Dummy user data for demonstration purposes
users = {"user": "password", "username": "password"}

@app.route('/')
def home():
    return render_template('index.html')  # Render the sign-in page

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and users[username] == password:
        return redirect(url_for('authenticated'))
    return redirect(url_for('home'))

@app.route('/authenticated')
def authenticated():
    return render_template('demo_upload.html')  # Render the authenticated page

if __name__ == '__main__':
    app.run(debug=True)

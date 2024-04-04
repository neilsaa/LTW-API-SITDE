from flask import Flask, request, render_template,redirect,flash
import requests
import json

app = Flask(__name__)

app.secret_key = 'Neil'
app.template_folder = 'templates'
base_url = 'http://127.0.0.1:5000/users'

@app.route('/')
def index():
    response = requests.get(base_url)

    if response.status_code == 200:
        users = response.json()
        return render_template('user.html', users=users)
    else:
        flash('Error connecting to the API')
    
    return render_template('user.html')

@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_email = request.form.get('user_email')
        user_password = request.form.get('user_password')
        if user_name and user_email and user_password:
            response = requests.post(base_url, json={
                'name': user_name,
                'email': user_email,
                'password': user_password
            })

            if response.status_code == 200:

                user = response
                flash(f'User {user["id"]} successfully')
            else:
                flash('Error connecting to the API')
                return render_template('add.html')
        else:
            flash('All fields are required')
            return render_template('add.html')
    else: 
        render_template('user/add.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001) 
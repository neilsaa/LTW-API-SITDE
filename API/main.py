from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

sqldbname = 'db/website.db'

@app.route('/users/<int:id>',methods=['GET'])
def get_user(id):
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE id = ?', (id,))
    user = cursor.fetchone()

    # users_list = []
    # for user in users:
    if user:
        user_dict = {
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'password': user[3]
        }
        # users_list.append(user_dict) 
        return jsonify(user_dict)
    


@app.route('/users/<int:id>',methods=['PUT'])
def update_user(id):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    user_name = request.json.get('name')
    user_email = request.json.get('email')
    user_password = request.json.get('password')
    if user_name and user_email and user_password:
        cur.execute('UPDATE user SET name = ?, email = ?, password = ? WHERE id = ?', (user_name, user_email, user_password, id))
        conn.commit()
        if cur.rowcount > 0:
          return jsonify({'message': 'User updated'})
        else:
          return 'User not found', 404
    else:
        return 'User name, email and password are required', 400

@app.route('/users/<int:id>',methods=['DELETE'])
def delete_user(id):
    conn = sqlite3.connect(sqldbname)
    cur = conn.cursor()
    cur.execute('DELETE FROM user WHERE id = ?', (id,))
    conn.commit()
    if cur.rowcount > 0:
        return jsonify({'message': 'User deleted'})
    else:
        return 'User not found', 404


@app.route('/users',methods=['POST'])
def add_user():
   conn = sqlite3.connect(sqldbname)
   cur = conn.cursor()
   user_name = request.json.get('name')
   user_email = request.json.get('email')
   user_password = request.json.get('password')
   if user_name and user_email and user_password:
     cur.execute('INSERT INTO user (name, email, password) VALUES (?, ?, ?)', (user_name, user_email, user_password))
     conn.commit()
     user_id = cur.lastrowid

     return jsonify({'id': user_id})
   else:
     return 'User name, email and password are required', 400
   
@app.route('/users',methods=['GET'])
def get_all_users():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user')
    users = cursor.fetchall()

    users_list = []
    for user in users:
        user_dict = {
            'id': user[0],
            'name': user[1],
            'email': user[2],
            'password': user[3]
        }
        users_list.append(user_dict) 
    return jsonify(users_list)


if __name__ == '__main__':
    app.run(debug=True)
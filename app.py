import os
from flask import Flask, render_template, Response, request, redirect, url_for, session, flash, send_from_directory, jsonify
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

app.secret_key = 'rahasia'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hictaskmanager'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pengguna WHERE email = %s AND password = %s', (email, password,))
        akun = cursor.fetchone()
        if akun:
            session['loggedin'] = True
            session['id_user'] = akun['id_user']
            session['email'] = akun['email']
            session['password'] = akun['password']
            session['nama'] = akun['nama']

            flash('Selamat Datang, ' + akun['nama'] + '!', 'success')

            return redirect(url_for('dashboard'))
        else:
            msg = 'Email atau Password Salah!'
    return render_template("login/login.html", msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'GET':
        return render_template('register.html', msg=msg)
    else:
        email = request.form['email']
        password = request.form['password']
        nama = request.form['nama']

        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO pengguna VALUES ("", %s, %s, %s) ''', (email,password,nama))
        mysql.connection.commit()
        msg = 'Register Berhasil!'
        cursor.close()
        flash('Registrasi Berhasil!.')
        return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM pengguna WHERE id_user = %s', (session['id_user'],))
        akun = cursor.fetchone()
        return render_template("aplikasi/dashboard.html", akun=akun)
    return redirect(url_for('login'))

@app.route('/daftartugas')
def daftartugas():
    return render_template('aplikasi/daftartugas.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id_user', None)
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
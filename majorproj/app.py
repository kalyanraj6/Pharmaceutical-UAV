from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import winsound
orders=[]
app = Flask(__name__)
app.secret_key = '#abc123456'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sikaj@954'
app.config['MYSQL_DB'] = 'Kalyan'
 
mysql = MySQL(app)
@app.route('/')
def cover():
    return render_template('home.html')
@app.route('/which')
def which():
    return render_template('which.html')
@app.route('/type',methods=['GET','POST'])
def type():
    name=request.form.get('submit_button')
    if(name=="User"):
        return render_template('login.html')
    else:
        return render_template('admin_login.html')
    return render_template('login.html')
@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']
    if(username=="admin" and password=="admin"):
        return render_template('admin.html')
    else:
         msg = 'Incorrect username / password !'
    return render_template('admin_login.html', msg = msg)
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('navi.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('which'))
 
@app.route('/sign', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and  'mobile' in request.form  and 'address' in request.form and 'name' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['mobile']
        address = request.form['address']
        name = request.form['name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s , % s , % s)', (username, email,password , phone, address,name ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('sign.html', msg = msg)


@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/recieve_order', methods=['get','post'])
def recieve_order():
    s=0
    lst=[]
    lst.append(request.form['name'])
    lst.append(request.form['cn'])
    lst.append(request.form['houseadd'])
    lst.append(request.form['pincode'])
    lst.append(request.form['Phone'])
    lst.append(request.form['medicines'])
    orders.append(lst) 
    s=1
    if s==1:
        winsound.PlaySound("beep.wav", winsound.SND_FILENAME)  
        s=0    
    return render_template('order.html')

@app.route('/order_recieved',methods=['get','post'])
def order_recieved():
    print(orders)
    return render_template('order_recieved.html',orders=orders)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/coordinates')
def coordinates():
    return render_template('coordinates.html')

@app.route('/auth',methods=['get','post'])
def auth():
    ms=''
    if request.method == 'POST' and 'otp' in request.form:
        a=request.form['otp']
        if len(a)>5 and int(a)>=100000 and int(a)<=999999:
            ms='OTP verified Successfully!!!'
        else:
            ms= 'Incorrect OTP!!! Check again' 
    return render_template('auth.html',ms=ms)
@app.route('/surveillance')
def surveillance():
    return render_template('surveillance.html')
if __name__=="__main__":
    app.run(debug=True)
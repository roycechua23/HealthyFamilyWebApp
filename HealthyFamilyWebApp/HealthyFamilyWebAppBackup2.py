#from flask import Flask, render_template, redirect, request, json
from flask import *
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash,check_password_hash
from flask.ext.bootstrap import Bootstrap


mysql = MySQL()
healthyfamily = Flask(__name__)
healthyfamily.secret_key= '&&&777@seven.!@ASDASD!(H&*@H*&FGH@12312$F*&R$&F21312!@&*)^+_ASBFSJBXZSNabdasidasdb122989a'
bootstrap = Bootstrap(healthyfamily)

# @healthyfamily.route("/resetpass")
# def resetpass():
#     conn=mysql.connect()
#     cursor=

# MySQL configurations
healthyfamily.config['MYSQL_DATABASE_USER'] = 'royce'
healthyfamily.config['MYSQL_DATABASE_PASSWORD'] = '261523'
healthyfamily.config['MYSQL_DATABASE_DB'] = 'healthy_family'
healthyfamily.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(healthyfamily)

@healthyfamily.route("/user/<name>")
def user(name):
    return render_template("user.html",name=name)

@healthyfamily.route("/")
def index():
    return render_template('index.html')

@healthyfamily.route("/ShowSignin")
def signin():
    return render_template('signin.html')

@healthyfamily.route("/validateLogin", methods=['GET','POST'])
def validate():
    if request.method == 'POST':
        try:
            # Extraction of username and password
            _username = request.form['inputUsername']
            _password = request.form['inputPassword']

            # First Test Code for login validation
            # print(_username,_password)
            # if _username == "royce236" and _password == "261523":
            #     return redirect("/main/{}".format(_username))
            # else:
            #     return "<h1>Wrong username or password </h2>"

            # Actual connection
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('usp_verifyUser',(_username,))
            data = cursor.fetchone()
            print(data[1])

            if check_password_hash(data[0],_password)==True:
                session['user'] = _username
                print(_username)
                return redirect('main/{}'.format(str(_username)))

            else:
                return render_template('error.html', error='Invalid username or password')

        except Exception as e:
            return render_template('error.html', error='Server connection error. Try again later')
    else:
        return abort(401)

@healthyfamily.route("/logout")
def logout():
    session.pop('user',None)
    return redirect('/')

@healthyfamily.route("/main/<username>")
def securelogin(username):
    if session.get('user')==username:
        print(username)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute("SELECT user_name FROM useraccount WHERE user_username='{}' ".format(username))
        name=cursor.fetchone()
        if name is None:
            return render_template('error.html', error='Unauthorized Access')
        else:
            return render_template("main.html", name=name[0], rows=loadRowOrders(), orders=loadRowContent())
    else:
        return render_template('error.html', error='Unauthorized Access')

def loadRowOrders():
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.callproc('usp_showOrders',(session.get('user'),))
    data=cursor.fetchall()
    print(data)
    cursor.close()
    conn.close()
    return len(data)

def loadRowContent():
    conn=mysql.connect()
    cursor = conn.cursor()
    # Solution is only temporary and limited to one order
    cursor.callproc('usp_showOrders', (session.get('user'),))

    data=cursor.fetchone()
    return data

@healthyfamily.route("/orderWindow")
def orderWindow():
    if session.get('user'):
        return render_template('orderwindow.html')
    else:
        return abort(401)

@healthyfamily.route("/processOrder",methods=['POST'])
def processOrder():
    if request.method == 'POST' and session.get('user'):

        _quantity = request.form['InputOrderQuantity']

        print("Username: ",session.get('user'),"Qty: ",_quantity)
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.callproc('usp_createOrder', (session.get('user'), _quantity))
        conn.commit()
        print("Transaction Successful!")
        cursor.close()
        conn.close()
        html="""<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        <h1 align=center>Request Processed </h1>
        <button class="btn btn-lg btn-primary btn-block" type="button" value="Input" onclick="window.close();">Confirm</button>
        """
        return html
    else:
        return abort(401)

@healthyfamily.route("/ShowSignup")
def signup():
    return render_template('signup.html')

# Failed code
# @healthyfamily.route("/createAccount", methods=['POST','GET'])
# def createAccount():
#     print("function launched!")
#
#     if request.method == 'POST':
#         print("Request Method is: {}".format(request.method))
#         try:
#             _name = request.form['inputName']
#             _username = request.form['inputUserName']
#             _mobileno = request.form['inputMobileno']
#             _telno = request.form['inputTelno']
#             _email = request.form['inputEmail']
#             _address = request.form['inputAddress']
#             _password = request.form['inputPassword']
#             print("All forms retrieved")
#             # validate the recieved values (Output should be true since all fields have values)
#             if _name and _username and _mobileno and _telno and _email and _address and _password:
#
#                 # Call MySQL
#                 #     conn = mysql.connect()
#                 #     cursor = mysql.get_db().cursor()
#                 conn = mysql.connect()
#                 cursor = conn.cursor()
#                 _hashed_password = generate_password_hash(_password)
#                 cursor.callproc('usp_createUser',
#                                 (_name, _username, _mobileno, _telno, _email, _address, _hashed_password))
#                 data = cursor.fetchall()
#
#                 if len(data) is 0:
#                     conn.commit()
#                     return redirect('/')
#                     # return json.dumps({'message': 'User created sucessfully !'})
#                 else:
#                     print("Something Wrong!")
#                     return json.dumps({'error': str(data[0])})
#             else:
#                 return json.dumps({'message': '<span>Enter the Required Fields</span>'})
#         except Exception as e:
#             print("Some error catched")
#             return json.dumps({'error': str(e)})
#         finally:
#             cursor.close()
#             conn.close()

@healthyfamily.route("/createAccount", methods=['POST','GET'])
def createAccount():
    if request.method == 'POST':
        _name = request.form['inputName']
        _username = request.form['InputUserName']
        _mobileno = request.form['inputMobileno']
        _telno = request.form['inputTelno']
        _email = request.form['inputEmail']
        _address=request.form['inputAddress']
        _password=request.form['inputPassword']
        print("Data Recieved in server")
        if _name and _username and _mobileno and _telno and _email and _address and _password:
            conn = mysql.connect()
            cursor=conn.cursor()
            print("connection opened")
            _hashed_password = generate_password_hash(_password)
            print(_hashed_password)
            cursor.callproc('usp_createUser',(_name,_username,_mobileno,_telno,_email,_address,_hashed_password))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                cursor.close()
                conn.close()
                print("connection closed")
                return redirect('/')
            else:
                return json.dumps({'error': str(data[0])})

        else:
            return json.dumps({'message': '<span>Enter the Required Fields</span>'})

    else:
        return abort(401)

if __name__ == '__main__':
    healthyfamily.run(debug=True)



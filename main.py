from flask import Flask
from flask import render_template
from flask import request
from flask import Response
from flask import redirect
from flask import session
import os
import pyodbc

conn=pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                        'Server=PRIYA1114;'
                        'Database=LoginInfo;'
                        'Trusted_Connection=yes;')


cursor=conn.cursor()

app=Flask(__name__)
app.secret_key=os.urandom(24)


@app.route('/')
def login(): 
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def homee():
    
    if 'user_id' in session:

        age=request.form.get('a')
        sex=request.form.get('s')
        cp=request.form.get('cp')
        tb=request.form.get('tb')
        ch=request.form.get('ch')
        rest=request.form.get('rest')
        fbs=request.form.get('thal')
        ei=request.form.get('ei')
        an=request.form.get('an')
        old=request.form.get('old')
        slope=request.form.get('slope')
        ca=request.form.get('ca')
        th=request.form.get('th')
        tar=request.form.get('tar')

        # payload={'age':age , 'sex':sex , 'cp':cp ,'trestbps':tb,'chol':ch,'restecg':rest,'fbs':fbs,'ei':ei,'an':an,'old':old,'slope':slope,'ca':ca,'thal':th,'target':tar}
        # r=request.post('https://127.0.0.1',json=payload)
        #json_object=r.json()
        #max1 =max(json_object[0],json_object[1],json_object[2],json_object[3])
        #max1=max1*100
        return render_template('home.html',data=0)
    else:
        return     render_template('/')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    passs=request.form.get('pass')
    cursor.execute("""select*from login1 where email like '{}' and pass like '{}'""".format(email, passs))
    employee = cursor.fetchall()
    session['user_id']=employee[0][0]
    if len(employee) > 0:
        return redirect('/home')
    else:
        return redirect('/')


@app.route('/reach',methods=['POST'])
def jump():
    return render_template('results.html')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


@app.route('/addUser', methods=['POST'])
def addUSer():

    name=request.form.get('n')
    Lastname = request.form.get('l')
    email = request.form.get('e')
    PN=request.form.get('p')
    dob=request.form.get('d')
    address=request.form.get('address')
    passs=request.form.get('a')
    cursor.execute("""Insert into adduser1 values('{}','{}','{}','{}','{}','{}','{}')""".format(name,Lastname,email,PN,dob,address,passs))
    cursor.execute("""Insert into login1 values('{}','{}')""".format(email,passs))

    conn.commit()
    return render_template("register.html", message="Hi ,'{}' you have been sucessfully register".format(name))

@app.route('/help')
def help():
    return render_template('Help.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/addFeed',methods=['POST'])
def addFeed():
    name = request.form.get('firstname')
    Lastname = request.form.get('lastname')
    email = request.form.get('mailid')
    country = request.form.get('country')
    feed = request.form.get('subject')
    cursor.execute("""Insert into feedback values('{}','{}','{}','{}','{}')""".format(name, Lastname, email,country,feed))
    conn.commit()
    return render_template("feedback.html",message="Hi ,'{}' Thank for giving us a feedback".format(name))

        


if __name__=="__main__":
    app.run(debug=True)

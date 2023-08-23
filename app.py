from flask import Flask,render_template,request,session,redirect
import DbHelper as dbh
app=Flask(__name__)

app.secret_key="ruchikruchik"

@app.route('/')
def home():
    if 'user' in session:
        return render_template("home.html",username=session['user'],isLogged=True)
    return render_template("login.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get("username")
        passsword=request.form.get("password")
        print(username,passsword)
        flag=dbh.is_valid(username,passsword)
        if flag==True:
            session['user']=username
            return redirect("/")
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route('/logout',methods=['GET'])
def logout():
    username=session['user']
    session.pop('user')
    dbh.sessionendTime(username)
    return redirect("/")


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form.get("username")
        passsword=request.form.get("password")
        print(username,passsword)
        dbh.registerUser(username,passsword)
        return redirect("/")
    else:
       return render_template("register.html")



@app.route('/saveContactDetails',methods=['POST'])
def saveContactDetails():
    data=request.get_json(force=True)
    print(data)
    name=data['name']
    email=data['email']
    phone=data['phone']

    dbh.saveContact(name=name,email=email,phone=phone)
    print(name,email,phone)
    return "Saved Successfully",200

@app.route('/fetchContactDetails',methods=['GET'])
def fetchContactDetails():
    return dbh.fetchContact()


@app.route('/aboutUs')
def aboutUs():
    return render_template("about.html")



if(__name__=='__main__'):
    app.run()
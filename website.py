from flask import Flask, request, render_template, redirect, session,send_file, flash
import database as db
import json

app = Flask(__name__)
app.secret_key='(\x89\x8e\xc4\xa1\xf4\xfd\xce@\xaf\xe5\xf6'

@app.route('/', methods=['GET','POST'])
def login():
    rform=request.form
    if request.method=='POST':
        email=rform['Email']
        password=rform['Passwort']
        login_bool=db.User.login(email,password) #prüft, ob login daten mit db übereinstimmen gibt True oder False
        if login_bool==True:
            session['logged_in']=True
            return redirect('/home')
        else:
            flash('Email oder Passwort falsch!')
    return render_template('login.j2')

@app.route('/pw-vergessen', methods=['GET','POST'])
def pw_vergessen():
    """nicht implementiert"""
    # if request.method == 'POST':
    #     rform=request.form
        # users=db.User.getall2Dict()
        # for user in users:
        #     if rform['Email'] == user['Email']:
        #         msg = Message("Hello",
        #           sender="KHL.Usermanagement@gmail.com",
        #           recipients=user['Email'])
        #         mail.send(msg)
    return render_template('pw_vergessen.j2')  

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    session['Admin']=False
    return redirect('/')

@app.route('/registrieren',methods=['GET','POST'])
def registrieren():
    """pw_validation=Passwortbestätigung"""
    if not session.get('logged_in'):
        return redirect('/')
    if request.method=='POST':
        rform=request.form
        email=rform['Email']
        password=rform['Passwort']
        pw_validation=rform['pw_validation']
        if password == pw_validation:
            db.User.regist(email,password) 
            users=db.User.getall2Dict()
            return render_template('usermanagement.j2', users=users)     
        else:
            flash('Passwörter stimmen nicht überein!')
    return render_template('registrieren.j2')

@app.route('/home',methods=['GET','POST'])
def home():
    if not session.get('logged_in'):
        return redirect('/')
    return render_template('home.j2')

@app.route('/admin_auth', methods=['GET','POST'])
def admin_auth():
    if not session.get('logged_in'):
        return redirect('/')
    if request.method=='POST':
        rform = request.form
        if 'pw' in rform:
            pw=rform['pw']
            admin_pw='123asdqweyxc'
            if pw != admin_pw:
                flash('Passwort ist falsch!')
            else:
                session['Admin']=True
                users=db.User.getall2Dict()
                return render_template('usermanagement.j2', users=users)
    return render_template('admin_auth.j2')

@app.route('/usermanagement', methods=['GET','POST'])
def usermanagement():
    if not session.get('logged_in'):
        return redirect('/')
    if not session.get('Admin'):
        return redirect('/admin_auth')
    if request.method=='POST':
        rform=request.form
        if "Button_del" in rform:
            print(db.User.delete(rform['Button_del']))
    users=db.User.getall2Dict()
    return render_template('usermanagement.j2', users=users)

@app.route('/test', methods=['GET','POST'])
def test():
    return render_template('test.j2')

if __name__=='__main__':
    app.run()
    #app.run(host='0.0.0.0', port=5000)
from flask import Flask,render_template,request
from flask import current_app as capp
from backend.influencer import *
from backend.sponsor import *
from backend.admin import *
from backend.models import *

@capp.route("/", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        role = int(request.form.get("Role"))
        uname = request.form.get("username")
        pwd = request.form.get("pwd")
        if role == 1:
            return a_profile(uname,pwd)
        if role == 2:
            usr = Inf_Info.query.filter_by(username=uname,password=pwd).first()
            if usr:
                if usr.flag == 0:
                    return i_profile(uname,pwd)
                else:
                    return render_template("login.html",msg="You have been flagged!!!")
            else:
                return render_template("login.html",msg="Influencer not found")
        if role == 3:
            usr = Spr_Info.query.filter_by(username=uname,password=pwd).first()
            if usr:
                if usr.flag == 0:
                    return s_profile(uname,pwd)
                else:
                    return render_template("login.html",msg="You have been flagged!!!")
            else:
                return render_template("login.html",msg="Sponsor not found")
    if request.method == "GET":
        a = Admin.query.all()
        if not a:
            a = Admin()
            db.session.add(a)
            db.session.commit()
        return render_template("login.html",msg="")    
    
@capp.route("/for_pwd", methods = ["GET","POST"])
def for_pwd():
    if request.method == "POST":
        role = int(request.form.get("Role"))
        uname = request.form.get("username")
        pwd1 = request.form.get("npwd-1")
        pwd2 = request.form.get("npwd-2")
        if pwd1 == pwd2:
            return render_template("login.html",msg="")
        else:
            return render_template("for_pwd.html",error="new passwords dont match each other")
    if request.method == "GET":
        return render_template("for_pwd.html",error="") 

@capp.route("/influencer", methods = ["GET","POST"])
def inf_register():
    if request.method == "POST":
        role = 2
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        exp = int(request.form.get("exp"))
        platform = request.form.get("radiob")
        smlink = request.form.get("smlink")
        fcount = int(request.form.get("fcount"))
        niche = request.form.get("niche")
        usrname = request.form.get("username")
        pwd = request.form.get("pwd")
        chkusr = Inf_Info.query.filter_by(username=usrname).first()
        if chkusr:
            return render_template("influencer.html",msg="User already exists")
        else:
            usr = Inf_Info(fname=fname,lname=lname,email=email,experience=exp,platform=platform,smlink=smlink,fcount=fcount,niche=niche,username=usrname,password=pwd)
            db.session.add(usr)
            db.session.commit()
            return render_template("login.html",msg="")
    if request.method == "GET":
        return render_template("influencer.html",msg="")

@capp.route("/sponsor", methods = ["GET","POST"])
def spr_register():
    if request.method == "POST":
        role = 3
        cname = request.form.get("cname")
        ind = request.form.get("ind")
        bud = int(request.form.get("bud"))
        email = request.form.get("email")
        usrn = request.form.get("username")
        pwd = request.form.get("pwd")
        chkspr = Spr_Info().query.filter_by(username=usrn,password=pwd).first()
        if chkspr:
            return render_template("sponsor.html",msg="Sponsor already exists")
        else:
            newspr = Spr_Info(cname=cname,industry=ind,budget=bud,email=email,username=usrn,password=pwd)
            db.session.add(newspr)
            db.session.commit()
            return render_template("login.html",msg="")
    if request.method == "GET":
        return render_template("sponsor.html",msg="")
from flask import Flask,render_template,request
from flask import current_app as capp
from datetime import date
from backend.models import *
import matplotlib
matplotlib.use('Agg')  # Switch to a non-interactive backend
import matplotlib.pyplot as plt


@capp.route("/sd_prof/<usr>/<pwd>", methods = ["GET","POST"])
def s_profile(usr,pwd):
    campaigns = fetch_camp(usr)
    user = Spr_Info.query.filter_by(username=usr,password=pwd).first()
    req = Request.query.filter_by(s_name=usr).all()
    return render_template("sd_prof.html",user=user.username,pwd=pwd,camp=campaigns,req=req)

@capp.route("/req/acc/<usr>/<int:rid>/<pwd>", methods = ["GET","POST"])
def s_profile_ra(usr,rid,pwd):
    campaigns = fetch_camp(usr)
    req = Request.query.filter_by(id=rid).first()
    camp = Campaigns.query.filter_by(id=req.c_id).first()
    camp.influencer_name = req.i_name
    reqs = Request.query.filter_by(c_id=camp.id).all()
    for req in reqs:
        db.session.delete(req)
    db.session.commit()
    user = Spr_Info.query.filter_by(username=usr,password=pwd).first()
    req = Request.query.filter_by(s_name=usr)
    return render_template("sd_prof.html",user=user.username,pwd=pwd,camp=campaigns,req=req)

@capp.route("/req/del/<usr>/<int:rid>/<pwd>", methods = ["GET","POST"])
def s_profile_rd(usr,rid,pwd):
    campaigns = fetch_camp(usr)
    req = Request.query.filter_by(id=rid).first()
    db.session.delete(req)
    db.session.commit()
    user = Spr_Info.query.filter_by(username=usr,password=pwd).first()
    req = Request.query.filter_by(s_name=usr).all()
    return render_template("sd_prof.html",user=user.username,pwd=pwd,camp=campaigns,req=req)

@capp.route("/spr/req/<usr>/<inf>/<cid>/<pwd>", methods = ["GET","POST"])
def s_req(usr,inf,cid,pwd):
    req = Request(c_id=cid,s_name=usr,i_name=inf)
    db.session.add(req)
    db.session.commit()
    fcamp = fetch_camp_nall(usr)
    camp = {}
    for key,value in fcamp.items():
        if value[10] == '1' and value[2] == '1':
            camp[key] = value
    inf = Inf_Info.query.all()
    return render_template("sd_find.html",user=usr,pwd=pwd,camp=camp,infl=inf)

def fetch_camp(user):
    campaigns = Campaigns.query.filter_by(s_name=user).all()
    camp_dict = {}
    for camp in campaigns:
        ads = Ad_req.query.filter_by(campaign_id=camp.id).all()
        ad_dict = {}
        tot_ad = 0.0
        c_ad = 0.0
        for ad in ads:
            if ad.id not in ad_dict.keys():
                ad_dict[ad.id] = [ad.tasks,ad.payment,ad.status]
                tot_ad += 1
                if ad.status == '2':
                    c_ad += 1
        if camp.id not in camp_dict.keys():
            if tot_ad != 0:
                camp.progress = (c_ad/tot_ad)*100
            else:
                camp.progress = 0.0
            camp_dict[camp.id] = [camp.name,camp.desc,camp.status,camp.niche,ad_dict,camp.influencer_name,f"{camp.progress:.2f}",camp.s_date,camp.e_date,camp.budget,camp.visibility,camp.goals,camp.flag]
    return camp_dict

def fetch_camp_nall(user):
    campaigns = Campaigns.query.filter(Campaigns.s_name!=user).all()
    camp_dict = {}
    for camp in campaigns:
        ads = Ad_req.query.filter_by(campaign_id=camp.id).all()
        ad_dict = {}
        tot_ad = 0.0
        c_ad = 0.0
        for ad in ads:
            if ad.id not in ad_dict.keys():
                ad_dict[ad.id] = [ad.tasks,ad.payment,ad.status]
                tot_ad += 1
                if ad.status == '2':
                    c_ad += 1
        if camp.id not in camp_dict.keys():
            if tot_ad != 0:
                camp.progress = (c_ad/tot_ad)*100
            else:
                camp.progress = 0.0
            if camp.progress == 100:
                camp.status = '3'
            camp_dict[camp.id] = [camp.name,camp.desc,camp.status,camp.niche,ad_dict,camp.influencer_name,f"{camp.progress:.2f}",camp.s_date,camp.e_date,camp.budget,camp.visibility,camp.goals,camp.flag]
    return camp_dict

def feth_spr(usr):
    spr = Spr_Info.query.filter_by(username=usr).first()
    return spr

@capp.route("/camp/add/<user>/<pwd>", methods = ["GET","POST"])
def handle_form(user,pwd):
    if request.method == "POST":
        name = request.form.get('cname')
        description = request.form.get('desc')
        start_date = request.form.get('sd')
        end_date = request.form.get('ed')
        if end_date < start_date:
            return render_template("campaigns.html",msg="Enter date properly",user=user,pwd=pwd,camp=campaign,req=req)
        budget = request.form.get('bud')
        visibility = request.form.get('vis')
        goals = request.form.get('goal')
        niche = request.form.get('niche')
        camp = Campaigns(s_name=user,name=name,desc=description,niche=niche,s_date=start_date,e_date=end_date,budget=budget,progress='0.0',visibility=visibility,goals=goals)
        db.session.add(camp)
        db.session.commit()
        campaign = fetch_camp(user)
        req = Request.query.filter_by(s_name=user)
        return render_template("campaigns.html",user=user,pwd=pwd,camp=campaign,req=req)

@capp.route("/camp/edit/<user>/<int:cid>/<pwd>", methods = ["GET","POST"])
def edit_form(user,cid,pwd):
    if request.method == "POST":
        name = request.form.get('cname')
        description = request.form.get('desc')
        start_date = request.form.get('sd')
        end_date = request.form.get('ed')
        if end_date < start_date:
            return render_template("campaigns.html",msg="Enter date properly",user=user,pwd=pwd,camp=campaign,req=req)
        budget = request.form.get('bud')
        visibility = request.form.get('vis')
        goals = request.form.get('goal')
        camp = Campaigns.query.filter_by(id=cid).first()
        camp.name = name
        camp.desc = description
        camp.s_date = start_date
        camp.e_date = end_date
        camp.budget = budget
        camp.visibility = visibility
        camp.goals = goals
        db.session.commit()
        campaign = fetch_camp(user)
        req = Request.query.filter_by(s_name=user)
        return render_template("campaigns.html",user=user,pwd=pwd,camp=campaign,req=req)

@capp.route("/camp/del/<user>/<int:camp_id>/<pwd>", methods = ["GET","POST"])
def camp_del(user,camp_id,pwd):
    camps = Campaigns.query.filter_by(id=camp_id)
    ads = Ad_req.query.filter_by(campaign_id=camp_id).all()
    for ad in ads:
        db.session.delete(ad)
    for camp in camps:
        db.session.delete(camp)
    db.session.commit()
    campaign = fetch_camp(user)
    req = Request.query.filter_by(s_name=user)
    return render_template("campaigns.html",user=user,pwd=pwd,camp=campaign,req=req)

@capp.route("/ad/del/<user>/<int:ad_id>/<pwd>", methods = ["GET","POST"])
def ad_del(user,ad_id,pwd):
    ad = Ad_req.query.filter_by(id=ad_id).first()
    db.session.delete(ad)
    db.session.commit()
    campaign = fetch_camp(user)
    req = Request.query.filter_by(s_name=user)
    return render_template("campaigns.html",user=user,pwd=pwd,camp=campaign,req=req)
    
@capp.route("/ad/add/<user>/<int:camp_id>/<pwd>", methods = ["GET","POST"])
def add_d(user,camp_id,pwd):
    if request.method == "POST":
        task = request.form.get("task")
        pay = request.form.get("pay")
        ad = Ad_req(campaign_id=camp_id,tasks=task,payment=pay)
        db.session.add(ad)
        db.session.commit()
        camp = fetch_camp(user)
        req = Request.query.filter_by(s_name=user)
        return render_template("campaigns.html",user=user,pwd=pwd,camp=camp,req=req)
    
@capp.route("/ad/edit/<user>/<pwd>", methods = ["GET","POST"])
def edit_d(user,pwd):
    if request.method == "POST":
        n_id = request.form.get("id")
        n_task = request.form.get("task")
        n_pay = request.form.get("pay")
        ad = Ad_req.query.filter_by(id=n_id).first()
        ad.id=n_id
        ad.tasks = n_task
        ad.payment = n_pay
        db.session.commit()
        camp = fetch_camp(user)
        req = Request.query.filter_by(s_name=user)
        return render_template("campaigns.html",user=user,pwd=pwd,camp=camp,req=req)

@capp.route("/sd_find/<user>/<pwd>", methods = ["GET","POST"])
def s_find(user,pwd):
    fcamp = fetch_camp_nall(user)
    camp = {}
    for key,value in fcamp.items():
        if value[10] == '1' and value[2] == '1':
            camp[key] = value
    inf = Inf_Info.query.all()
    if request.method == "POST":
        search = request.form.get("search")
        filter = request.form.get("fil")
        if filter == '1':
            if search:
                n_inf = Inf_Info.query.filter_by(username=search).all()
                return render_template("sd_find.html",user=user,pwd=pwd,camp=None,infl=n_inf)
            return render_template("sd_find.html",user=user,pwd=pwd,camp=None,infl=inf)
        elif filter == '2':
            if search:
                ncamp = {}
                for key,value in camp.items():
                    if value[0] == search:
                        ncamp[key] = value
                return render_template("sd_find.html",user=user,pwd=pwd,camp=ncamp,infl=None)
            return render_template("sd_find.html",user=user,pwd=pwd,camp=camp,infl=None)
    if request.method == "GET":
        return render_template("sd_find.html",user=user,pwd=pwd,camp=camp,infl=inf)
    
@capp.route("/sd_find/req/<user>/<pwd>", methods = ["GET","POST"])
def req(user,pwd):
    fcamp = fetch_camp_nall(user)
    camp = {}
    for key,value in fcamp.items():
        if value[10] == '1' and value[2] == '1':
            camp[key] = value
    inf = Inf_Info.query.all()
    cid = int(request.form.get('cid'))
    iuname = request.form.get('iuname')
    req = Request(s_name=user,c_id=cid,i_name=iuname)
    return render_template("sd_find.html",user=user,pwd=pwd,camp=camp,infl=inf)
    
@capp.route("/sd_camp/<usr>/<pwd>", methods = ["GET","POST"])
def camps(usr,pwd):
    campaigns = fetch_camp(usr)
    user = Spr_Info.query.filter_by(username=usr,password=pwd).first()
    return render_template("campaigns.html",user=user.username,pwd=pwd,camp=campaigns)

def gen_spr_summ(usr):
    camp = fetch_camp(usr)
    comp = 0
    ncomp = 0
    pend = 0
    for key,value in camp.items():
        if value[2] == '1':
            pend += 1
        elif value[2] == '2':
            ncomp += 1
        else:
            comp += 1
    path = "static/img/spr/"
    label_a = ['completed','not completed']
    for key,value in camp.items():
        acomp = 0
        ancomp = 0
        for k,v in value[4].items():
            if v[2] == '1':
                ancomp += 1
            else:
                acomp += 1
        data = [acomp,ancomp]
        if value[4]:
            plt.bar(label_a,data,width=0.3,color="maroon")
            plt.savefig(path + value[0] + '.jpg')
            plt.clf()
    label_s = ['completed','not completed','pending']
    plt.bar(label_s,[comp,ncomp,pend],width=0.3,color="blue")
    plt.savefig(path + usr + '.jpg')
    plt.clf()
  
@capp.route("/sd_stat/<usr>/<pwd>", methods = ["GET","POST"]) 
def stats(usr,pwd):
    gen_spr_summ(usr)
    camp = fetch_camp(usr)
    return render_template("sd_stats.html",user=usr,pwd=pwd,camp=camp)
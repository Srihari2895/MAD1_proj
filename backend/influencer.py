from flask import Flask,render_template,request
from flask import current_app as capp
from backend.models import *
from backend.sponsor import *
import matplotlib
matplotlib.use('Agg')  # Switch to a non-interactive backend
import matplotlib.pyplot as plt


@capp.route("/id_prof/<usr>/<pwd>", methods = ["GET","POST"])
def i_profile(usr,pwd):
    camp = fetch_camp_i(usr)
    req = Request.query.filter_by(i_name=usr)
    return render_template("id_prof.html",user=usr,pwd=pwd,camp=camp,req=req)

def fetch_camp_i(user):
    campaigns = Campaigns.query.filter_by(influencer_name=user).all()
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
            camp_dict[camp.id] = [camp.name,camp.desc,camp.status,camp.niche,ad_dict,camp.influencer_name,f"{camp.progress:.2f}",camp.s_date,camp.e_date,camp.budget,camp.visibility,camp.goals]
    return camp_dict

def fetch_camp_n(niche):
    campaigns = Campaigns.query.filter_by(niche=niche).all()
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
            camp_dict[camp.id] = [camp.name,camp.desc,camp.status,camp.niche,ad_dict,camp.influencer_name,f"{camp.progress:.2f}",camp.s_date,camp.e_date,camp.budget,camp.visibility,camp.goals,camp.s_name]
    return camp_dict

@capp.route("/id_find/<usr>/<pwd>", methods = ["GET","POST"])
def i_find(usr,pwd):
    inf = Inf_Info.query.filter_by(username=usr,password=pwd).first()
    fcamp = fetch_camp_n(inf.niche)
    camp = {}
    for key,val in fcamp.items():
        if val[10] == '1' and val[2] == '1':
            camp[key] = val
    if request.method == "POST":
        search = request.form.get("searchField")
        new_cd = {}
        for key,value in camp.items():
            if value[0] == search or value[12] == search:
                new_cd[key] = value
        return render_template("id_find.html",user=usr,pwd=pwd,camp=new_cd,nic=inf.niche)
    if request.method == "GET":
        return render_template("id_find.html",user=usr,pwd=pwd,camp=camp,nic=inf.niche)
    
@capp.route("/inf/req/<usr>/<spr>/<cid>/<pwd>", methods = ["GET","POST"])
def i_req(usr,spr,cid,pwd):
    req = Request(c_id=cid,s_name=spr,i_name=usr)
    db.session.add(req)
    db.session.commit()
    #pwd = request.form.get('pwd')
    print(pwd)
    inf = Inf_Info.query.filter_by(username=usr,password=pwd).first()
    print(inf)
    fcamp = fetch_camp_n(inf.niche)
    camp = {}
    for key,val in fcamp.items():
        if val[10] == '1' and val[2] == '1':
            camp[key] = val
    return render_template("id_find.html",user=usr,pwd=pwd,camp=camp,nic=inf.niche)

@capp.route("/infreq/acc/<usr>/<rid>/<pwd>", methods = ["GET","POST"])
def reqa(usr,rid,pwd):
    camp = fetch_camp_i(usr)
    req = Request.query.filter_by(id=rid).first()
    camp = Campaigns.query.filter_by(id=req.c_id)
    camp.influencer_name = req.i_name
    reqs = Request.query.filter_by(c_id=camp.id)
    for req in reqs:
        db.session.delete(req)
    db.session.commit()
    req = Request.query.filter_by(i_name=usr)
    return render_template("id_prof.html",user=usr,pwd=pwd,camp=camp,req=req)

@capp.route("/infreq/del/<usr>/<rid>/<pwd>", methods = ["GET","POST"])
def reqd(usr,rid,pwd):
    camp = fetch_camp_i(usr)
    req = Request.query.filter_by(id=rid).first()
    db.session.delete(req)
    db.session.commit()
    req = Request.query.filter_by(i_name=usr)
    return render_template("id_prof.html",user=usr,pwd=pwd,camp=camp,req=req)

@capp.route("/check/<user>/<pwd>", methods = ["GET","POST"])
def change_stat(user,pwd):
    stat = request.form.get('stat')
    id = request.form.get('id')
    ad = Ad_req.query.filter_by(id=id).first()
    ad.status = stat
    db.session.commit()
    camp = fetch_camp_i(user)
    req = Request.query.filter_by(i_name=user)
    return render_template("id_prof.html",user=user,pwd=pwd,camp=camp,req=req)
    
    
def gen_inf_summ(usr):
    camp = fetch_camp_i(usr)
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
    path = "static/img/inf/"
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
    
@capp.route("/id_stat/<usr>/<pwd>", methods = ["GET","POST"]) 
def istats(usr,pwd):
    gen_inf_summ(usr)
    camp = fetch_camp_i(usr)
    return render_template("id_stats.html",user=usr,pwd=pwd,camp=camp)
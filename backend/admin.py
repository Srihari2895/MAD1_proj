from flask import Flask,render_template,request
from flask import current_app as capp
from backend.models import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

@capp.route("/ad_prof/<usr>/<pwd>", methods = ["GET","POST"])
def a_profile(usr,pwd):
    if request.method =='POST':
        f_inf = request.form.get("iname")
        f_spr = request.form.get("sname")
        print(f_spr)
        if f_inf:
            flagi = Inf_Info.query.filter_by(username=f_inf).first()
            flagi.flag = 0
            db.session.commit()
        if f_spr:
            flags = Spr_Info.query.filter_by(username=f_spr).first()
            flags.flag = 0
            db.session.commit()
    inf = Inf_Info.query.filter_by(flag=1).all()
    spr = Spr_Info.query.filter_by(flag=1).all()
    return render_template("admin_prof.html",user=usr,pwd=pwd,infl=inf,sprs=spr)

@capp.route("/admin/users/<usr>/<pwd>", methods = ["GET","POST"])
def a_users(usr,pwd):
    if request.method =='POST':
        f_inf = request.form.get("iname")
        f_spr = request.form.get("sname")
        print(f_spr)
        if f_inf:
            flagi = Inf_Info.query.filter_by(username=f_inf).first()
            flagi.flag = 1
            db.session.commit()
        if f_spr:
            flags = Spr_Info.query.filter_by(username=f_spr).first()
            flags.flag = 1
            db.session.commit()
    inf = Inf_Info.query.filter_by(flag=0).all()
    spr = Spr_Info.query.filter_by(flag=0).all()
    return render_template("admin_users.html",usr=usr,pwd=pwd,infl=inf,sprs=spr)
    
def fetch_camp_flag(f):
    campaigns = Campaigns.query.filter_by(flag=f).all()
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
 
@capp.route("/ad_camp/<usr>/<pwd>", methods = ["GET","POST"])
def camp(usr,pwd):
    if request.method == "POST":
        ukey = request.form.get("ukey")
        fkey = request.form.get("fkey")
        if ukey:
            camp = Campaigns.query.filter_by(id=ukey).first()
            print(camp.flag)
            camp.flag = 0
            print(camp.flag)
            db.session.commit()
        if fkey:
            camp = Campaigns.query.filter_by(id=fkey).first()
            print(camp.flag)
            camp.flag = 1
            print(camp.flag)
            db.session.commit()
    ucamps = fetch_camp_flag(0)
    fcamps = fetch_camp_flag(1)
    return render_template("admin_camp.html",user=usr,pwd=pwd,ucamp=ucamps,fcamp=fcamps)

def gen_spr_summ(usr):
    camp = fetch_camp_flag(usr)
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
        print(data)
        if value[4]:
            plt.bar(label_a,data,width=0.3,color="maroon")
            plt.savefig(path + value[0] + '.jpg')
            plt.clf()
    label_s = ['completed','not completed','pending']
    plt.bar(label_s,[comp,ncomp,pend],width=0.3,color="blue")
    plt.savefig(path + usr + '.jpg')
    plt.clf()

@capp.route("/ad_stat/<usr>/<pwd>", methods = ["GET","POST"]) 
def astats(usr,pwd):
    sprs = Spr_Info.query.all()
    for spr in sprs:
        gen_spr_summ(spr.username)
    infs = Inf_Info.query.all()
    print(infs)
    for inf in infs:
        gen_inf_summ(inf.username)
    campu = fetch_camp_flag(0)
    campf = fetch_camp_flag(1)
    return render_template("adm_stats.html",user=usr,pwd=pwd,campu=campu,sprs=sprs,infl=infs,campf=campf)
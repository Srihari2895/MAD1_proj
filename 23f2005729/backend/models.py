from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Admin(db.Model):
    username = db.Column(db.String,primary_key=True,default="Admin_mad1")
    pwd = db.Column(db.String,default="0a1d2m3i4n5")
    
class Inf_Info(db.Model):
    __tablename__ = "inf_info"
    role = db.Column(db.Integer,default=2)
    fname = db.Column(db.String,nullable=False)
    lname = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)
    experience = db.Column(db.Integer,nullable=False)
    platform = db.Column(db.String,nullable=False)
    smlink = db.Column(db.String,nullable=False)
    fcount = db.Column(db.Integer,nullable=False)
    rating = db.Column(db.Float,nullable=True)
    earning = db.Column(db.Float,nullable=True)
    username = db.Column(db.String,primary_key=True)
    password = db.Column(db.String,nullable=False)
    flag = db.Column(db.Integer,default=0,nullable=False)
    niche = db.Column(db.String,nullable=True)
    campaign = db.relationship("Campaigns",cascade="all,delete",backref="inf_info")
    request =  db.relationship("Request",cascade="all,delete",backref="inf_info")
    
class Spr_Info(db.Model):
    __tablename__ = "spr_info"
    cname = db.Column(db.String,nullable=False)
    industry = db.Column(db.String,nullable=False)
    budget = db.Column(db.Integer,nullable=False)
    email = db.Column(db.String,nullable=False)
    username = db.Column(db.String,primary_key=True)
    password = db.Column(db.String,nullable=False)
    flag = db.Column(db.Integer,default=0,nullable=False)
    campaign = db.relationship("Campaigns",cascade="all,delete",backref="spr_info")
    request = db.relationship("Request",cascade="all,delete",backref="spr_info")
    
class Campaigns(db.Model):
    __tablename__ = "campaigns"
    id = db.Column(db.Integer,primary_key=True)
    s_name = db.Column(db.String,db.ForeignKey("spr_info.username"))
    name = db.Column(db.String,nullable=False)
    desc = db.Column(db.String,nullable=False)
    s_date = db.Column(db.String,nullable=False)
    e_date = db.Column(db.String,nullable=False)
    budget = db.Column(db.Integer,nullable=False)
    visibility = db.Column(db.String,nullable=False)
    goals = db.Column(db.String,nullable=False)
    status = db.Column(db.String,default="1")
    progress = db.Column(db.String,nullable=False)
    influencer_name = db.Column(db.String,db.ForeignKey("inf_info.username"),nullable=True)
    flag = db.Column(db.Integer,default=0,nullable=False)
    niche = db.Column(db.String,nullable=True)
    ad_req = db.relationship("Ad_req",cascade="all,delete",backref="campaigns")
    req = db.relationship("Request",cascade="all,delete",backref="campaigns")
    
class Ad_req(db.Model):
    __tablename__ = "ad_requests"
    id = db.Column(db.Integer,primary_key=True)
    campaign_id = db.Column(db.Integer,db.ForeignKey("campaigns.id"),nullable=False)
    status = db.Column(db.String,default="1")
    tasks = db.Column(db.String,nullable=False)
    payment = db.Column(db.Float,nullable=False)
    
class Request(db.Model):
    __tablename__="request"
    id = db.Column(db.Integer,primary_key=True)
    c_id = db.Column(db.Integer,db.ForeignKey("campaigns.id"),nullable=False)
    s_name = db.Column(db.String,db.ForeignKey("spr_info.username"))
    i_name = db.Column(db.String,db.ForeignKey("inf_info.username"),nullable=True)
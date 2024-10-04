from flask_restful import Api,Resource,reqparse
from backend.models import *

api = Api()

lp = reqparse.RequestParser()
lp.add_argument("cname")
lp.add_argument("industry")
lp.add_argument("budget")
lp.add_argument("email")
lp.add_argument("password")
lp.add_argument("flag")

class SprApi(Resource):
    def get(self,user,pwd):
        sprs = Spr_Info.query.filter_by(username=user,password=pwd).first()
        spr = {}
        spr["username"] = sprs.username
        spr["cname"] = sprs.cname
        spr["industry"] = sprs.industry
        spr["budget"] = sprs.budget
        spr["email"] = sprs.email
        spr["password"] = sprs.password
        spr["flag"] = sprs.flag
        spl = [spr]
        return spl
    
    def post(self,user):
        data = lp.parse_args()
        new_spr = Spr_Info(username=user,cname=data["cname"],industry=data["industry"],budget=data["budget"],email=data["email"],password=data["password"],flag=data["flag"])
        db.session.add(new_spr)
        db.session.commit()
        return "Sponsor created",201
    
    def put(self,user):
        data = lp.parse_args()
        spr = Spr_Info.query.filter_by(username=user).first()
        if spr:
            spr.cname=data["cname"]
            spr.industry=data["industry"]
            spr.budget=data["budget"]
            spr.email=data["email"]
            spr.password=data["password"]
            spr.flag=data["flag"]
            db.session.commit()
            return "Sponsor details edited",200
        else:
            return "Sponsor not found",404
    
    def delete(self,user):
        data = lp.parse_args()
        spr = Spr_Info.query.filter_by(username=user).first()
        if spr:
            db.session.delete(spr)
            db.session.commit()
            return "Sponsor deleted",205
        else:
            return "Sponsor not found",404
    
api.add_resource(SprApi,"/api/spr/<user>/<pwd>","/api/spr/<user>")   
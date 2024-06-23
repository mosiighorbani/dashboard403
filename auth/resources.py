from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required
from app import db
from .models import UserModel
from .schemas import UserSchema
from blocklist import BLOCKLIST



# authApi = Blueprint("Auth", "authes", subdomain="api" , description="Operations on Authentication")
authApi = Blueprint("Auth", "authes", description="Operations on Authentication")



@authApi.route("/api/auth/register")
class UserRegister(MethodView):
    @authApi.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.phone == user_data["phone"]).first():
            abort(409, message = "a user with that phone is already exixts")
        # 
        user = UserModel()
        user.name = user_data["name"]
        user.phone = user_data["phone"]
        user.set_password(user_data["password"])
        # 
        db.session.add(user)
        db.session.commit()
        # 
        return {"message" : "User is Created Successfully"}, 201
    


@authApi.route("/api/auth/login")
class UserLogin(MethodView):
    @authApi.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.phone == user_data["phone"]).first()
        if user and user.check_password(user_data["password"]):
            print(user)
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token" : access_token, "refresh_token" : refresh_token}
        abort(401, message="Invalid Credentilas")


@authApi.route("/api/auth/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token":new_token}, 200


@authApi.route("/api/auth/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message":"Successfully Logged Out"}, 200
    

@authApi.route("/api/auth/user/<int:user_id>")
class user(MethodView):
    """for testing in development project"""
    @authApi.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
            return {"message" : "User is Deleted Successfully"}, 200
        except Exception as er:
            abort(401, message=f"Error {er} is happened !")

    
    





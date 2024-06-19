from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required
from app import db
from .models import UserModel
from .schemas import UserSchema
from blocklist import BLOCKLIST



authApi = Blueprint("Users", "users", description="Operations on users")



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
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token" : access_token, "refresh_token" : refresh_token}
        abort(401, message="Invalid Credentilas")





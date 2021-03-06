"""
    Defines APIs for user handling.
"""
from flask import request, jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from application.models.user import User, Role
from application.database import db
from application.auth import hasrole


nameArg = reqparse.Argument(name='name', type=str, required=True, 
help='No name provided', location='json')
emailArg = reqparse.Argument(name='email', type=str, required=True, 
help='No email provided', location='json')
pwdArg = reqparse.Argument(name='password', type=str, required=True, 
help='No password provided', location='json')


"""
    Defines routes for users listing and user adding.
"""
class UsersAPI(Resource):

    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(nameArg)
        self.reqparse.add_argument(emailArg)
        self.reqparse.add_argument(pwdArg)
        super(UsersAPI, self).__init__()

    def post(self):
        data = request.get_json()
        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return "User " + user.username + " has been saved", 201

    @jwt_required()
    def get(self):
        users = User.find_all()
        if users:
            return users, 200
        else:
            return [], 200


"""
    Defines routes for user editing and user viewing.
"""
class UserAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(nameArg)
        self.reqparse.add_argument(emailArg)
        super(UserAPI, self).__init__()

    def get(self, id):
        user = User.find_by_id(id)
        if not user:
            return "User not found", 404
        else:
            return user.serializable(), 200


    def put(self, id):
        user = User.find_by_id(id)        
        if not user:
            return "User not found", 404
        else:
            data = request.get_json()        
            self.reqparse.parse_args()
            user.username = data['username']
            user.email = data['email']
            db.session.add(user)
            db.session.commit()
            return user, 200
            # todo: roles
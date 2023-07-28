from flask import request, Response, json, Blueprint
from src.models.user_model import User
from src import bcrypt, db
from datetime import datetime
import jwt
import os

# user controller blueprint to be registered with api blueprint
users = Blueprint("users", __name__)

# route for signup api/users/signup
@users.route('/signup', methods = ["POST"])
def handle_signup():
    try: 
        # first validate required use parameters
        data = request.json
        if "firstname" in data and "lastname" and data and "email" and "password" in data:
            # validate if the user exist 
            user = User.query.filter_by(email = data["email"]).first()
            # usecase if the user doesn't exists
            if not user:
                # creating the user instance of User Model to be stored in DB
                user_obj = User(
                    firstname = data["firstname"],
                    lastname = data["lastname"],
                    email = data["email"],
                    # hashing the password
                    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
                )
                db.session.add(user_obj)
                db.session.commit()

                # lets generate jwt token
                payload = {
                    'iat': datetime.utcnow(),
                    'user_id': str(user_obj.id).replace('-',""),
                    'firstname': user_obj.firstname,
                    'lastname': user_obj.lastname,
                    'email': user_obj.email,
                }
                token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')
                return Response(
                response=json.dumps({'status': "success",
                                    "message": "User Sign up Successful",
                                    "token": token}),
                status=201,
                mimetype='application/json'
            )
            else:
                print(user)
                # if user already exists
                return Response(
                response=json.dumps({'status': "failed", "message": "User already exists kindly use sign in"}),
                status=409,
                mimetype='application/json'
            )
        else:
            # if request parameters are not correct 
            return Response(
                response=json.dumps({'status': "failed", "message": "User Parameters Firstname, Lastname, Email and Password are required"}),
                status=400,
                mimetype='application/json'
            )
        
    except Exception as e:
        return Response(
                response=json.dumps({'status': "failed", 
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )

# route for login api/users/signin
@users.route('/signin', methods = ["POST"])
def handle_login():
    try: 
        # first check user parameters
        data = request.json
        if "email" and "password" in data:
            # check db for user records
            user = User.query.filter_by(email = data["email"]).first()

            # if user records exists we will check user password
            if user:
                # check user password
                if bcrypt.check_password_hash(user.password, data["password"]):
                    # user password matched, we will generate token
                    payload = {
                        'iat': datetime.utcnow(),
                        'user_id': str(user.id).replace('-',""),
                        'firstname': user.firstname,
                        'lastname': user.lastname,
                        'email': user.email,
                        }
                    token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')
                    return Response(
                            response=json.dumps({'status': "success",
                                                "message": "User Sign In Successful",
                                                "token": token}),
                            status=200,
                            mimetype='application/json'
                        )
                
                else:
                    return Response(
                        response=json.dumps({'status': "failed", "message": "User Password Mistmatched"}),
                        status=401,
                        mimetype='application/json'
                    ) 
            # if there is no user record
            else:
                return Response(
                    response=json.dumps({'status': "failed", "message": "User Record doesn't exist, kindly register"}),
                    status=404,
                    mimetype='application/json'
                ) 
        else:
            # if request parameters are not correct 
            return Response(
                response=json.dumps({'status': "failed", "message": "User Parameters Email and Password are required"}),
                status=400,
                mimetype='application/json'
            )
        
    except Exception as e:
        return Response(
                response=json.dumps({'status': "failed", 
                                     "message": "Error Occured",
                                     "error": str(e)}),
                status=500,
                mimetype='application/json'
            )

import sys
sys.path.append('../')

import config
import jwt
import database
from database import users
from send_mail import *


#Any functions that are not executed directly by the api
db = database.db

#Generated a JWT token signed with a secret key and the users email as the payload
#RETURNS JWT token
def genJWT(email):
    enc = jwt.encode({"email": email}, config.JWT_KEY, algorithm="HS256")
    return enc


#Decode a JWT token using a secret key
#RETURNS JWT token
def decodeJWT(token):
    try:
        data = jwt.decode(token, config.JWT_KEY, algorithms=["HS256"])
        return data
    except:
        return None

#Sends a OTC to the users email using the send_email functions
def sendotc(email, code):
    print(f'email is {email}')
    message = email_confirmation_message(code)
    send_email(email, message, "Confirmation Code")

#Expires the OTC by deleting its entry from the database
def expire(mail, otc):
    # query gives a list of users
    u = users.query.filter_by(email = mail, tmp = 1, otc = otc)
    if (not u):
        db.session.delete(u[0])
        db.session.commit()


#Validates if the token supplied by the frontend is a valid jwttoken
#ON SUCCESS returns 1
#ON FAILURE returns 0
def validate(jwttoken):
    data = jwt.decode(jwttoken, config.JWT_KEY, algorithms=["HS256"])
    email_recv = data['email']

    user = users.query.filter_by(email = email_recv, tmp = 0, token = jwttoken).all()
    if (user):
        return 1

    return 0

import sys

sys.path.append('../')

import json
import flask
from flask_sqlalchemy import SQLAlchemy
import math, random
import database
from database import users
import config
from functions.helpers import *
from functions.mutex import CricticalSection
from functions.funcs import *
from functions.wishlist import *
from threading import Timer
from send_mail import *
from datetime import datetime
from functions.reviewRatingFunc import *
from functions.banlist import *
from database import movies
from sqlalchemy import or_
from flask import Flask
from flask import request, Response



app = database.app
db = database.db

critsec = CricticalSection()



#Just to check backend is alive
def alive():

    resp = "I am alive!"
    return resp, 200


#The function which returns the saved reccomendations to the suggestions api
#ON SUCCESS returns [[id, name, genre, director, ...], [id, name, genre, director, ...] ...]

def get_recommendations(id):
    # Get the index of the movie that matches the title
    idx = config.indices[id]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(config.cosine_sim2[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:6]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    return config.metadata['name'].iloc[movie_indices]



#The api for getting similar movies for a particular movie using machine learning
#METHOD: POST
#Data body: {'username': '<username', 'movieId': <id>}
#ON SUCCESS returns [[id, name, genre, director, ...], [id, name, genre, director, ...] ...]
#ON FAILURE returns {"result": "failure", "message": "<message>"}
def suggestions():
    mId = request.get_json()['movieId']
    usrname = request.get_json()['username']

    #If movie id is not provided
    if (not mId):
        resp = flask.make_response({"result": "failure", "message": "Unable to perform action"})
        return resp, 400

    #Gets movie by searching for its id
    movie = movies.query.filter_by(id = mId).all()

    #Gets the reccomendations for a movie using machine learning
    robj = get_recommendations(movie[0].id)

    reccomendations = robj.values

    #Gets the top 6 reccommended movies
    recmovies = movies.query.filter(or_(movies.name == reccomendations[0], movies.name == reccomendations[1], movies.name == reccomendations[2], movies.name == reccomendations[3], movies.name == reccomendations[4])).all()
    resp = []

    #Adds reccommended movies to response
    for m in recmovies:
        rating = getRating(usrname, m.id)
        resp.append([m.id, m.name, m.genre, m.director, m.actor, m.poster, m.description, rating, m.year])


    return json.dumps(resp)





#The api for updating your profile
#METHOD: POST
#Data body: {"token": token, "oldPassword": password, "newPassword": password, "confirmedPassword": password}
#ON SUCCESS returns {"result": "success", "message": "<message>"}
#ON FAILURE returns {"result": "failure", "message": ...}
def updateprofile():
    token_recv = request.get_json()['token']
    oldpasswd = request.get_json()['oldPassword']
    passwd = request.get_json()['newPassword']
    passwd2 = request.get_json()['confirmedPassword']

    pflag = 0

    #Decodes the recieved jwt token
    if (token_recv):
        data = decodeJWT(token_recv)

    #If the recvied token is not the correct token
    if (data is None):
        resp = flask.make_response({"result": "failure", "message": "Unable to perform action"})
        return resp, 400

    user  = users.query.filter_by(email = data['email'], tmp = 0, token = token_recv).all()


    #If the user enters the wrong password
    if (oldpasswd != user[0].pass_hash.strip()):
        resp = flask.make_response({"result": "failure", "message": "Please enter the correct password"})
        return resp, 400

    if (oldpasswd and passwd and passwd2):
        res = updatepasswd(token_recv, passwd, passwd2)
        pflag = 1

    if (res):
        resp = flask.make_response({"result": "success", "message": "You have successfully changed your account details"})

        if (token_recv):
            data = decodeJWT(token_recv)

        if (data is None):
            resp = flask.make_response({"result": "failure", "message": "Unable to perform action"})
            return resp, 400

        user  = users.query.filter_by(email = data['email'], tmp = 0, token = token_recv).all()
        usrname = user[0].username

        #Generates alert email to send to user
        if (pflag):
            msg = profile_edit_mail_message(usrname, datetime.today().strftime('%Y-%m-%d'), 'password')


        #Sends update email to users email notifying them of the new activity
        send_email(data['email'], msg, 'Your account details have been changed')

        return resp, 200

    resp = flask.make_response({"result": "failure", "message": "Unable to perform action"})
    return resp, 400



#The function for updating your password
#ON SUCCESS returns 1
#ON FAILURE returns 0
def updatepasswd(token_recv, passwd, passwd2):

    if (passwd != passwd2):
        return 0

    #Checks if the user is logged in to this account by decoding JWT
    data = decodeJWT(token_recv)
    if (data is None):
        return 0

    email_recv = data['email']

    user = users.query.filter_by(email = email_recv, tmp = 0, token = token_recv).all()

    #Updates password
    if (user):
        user[0].pass_hash = passwd
        db.session.commit()
        return 1

    return 0




#The api for logging out of your profile
#METHOD: POST
#Data body: {"token": token}
#ON SUCCESS returns {"result": "success", "message": "<message>"}
#ON FAILURE returns {"result": "failure", "message": ...}
def logout():
    token_recv = request.get_json()['token']

    #Decode JWT token and if its incorrect return a failure message
    data = decodeJWT(token_recv)
    if (data is None):
        resp = flask.make_response({"result": "failure", "message": "Unable to perform action"})
        return resp, 400


    email_recv = data['email']

    user = users.query.filter_by(email = email_recv, tmp = 0, token = token_recv).all()

    #If a user by the name and token exists and is logged in remove the token from the user database
    if (user):
        user[0].token = None
        db.session.commit()
        resp = flask.make_response({"result": "success", "message": "You have successfully logged out"})
        return resp, 200

    #If the user is not logged in but tries to log out
    resp = flask.make_response({"result": "failure", "message": "You are not logged in as this user"})
    return resp, 400



#The api for logging into an account. The login button should link to this.
#METHOD: POST
#Data body: {'email': <email>, 'pass': <password>
#ON SUCCESS returns {"result": "success", "message": "Account created!"}
#ON FAILURE returns {"result": "failure", "message": ...}
def auth():
    email_recv = request.get_json()['email']
    pass_hash_recv = request.get_json()['password']

    #Gets user from database
    user = users.query.filter_by(email = email_recv, tmp = 0, pass_hash = pass_hash_recv).all()

    #If the username or password does not match
    if (not user):
        resp = flask.make_response({"result": "failure", "message": "Email or Password does not match!"})

        resp.headers['content_type'] = 'application/json'
        return resp, 400

    #Generates JWT token using secret and attaches it to user in database
    # JWT_token = genJWT(user[0].email).decode()
    JWT_token = genJWT(user[0].email)
    user[0].token = JWT_token
    db.session.commit()

    resp = flask.make_response({"result": "success", "token": JWT_token, "username": user[0].username})
    resp.headers['content_type'] = 'application/json'
    return resp, 200



#The api for changing your password if a user ha
#METHOD: POST
#Data body: {'email': <email>, 'password': <password>, 'paassword2': <password>, 'verificationCode': <code>}
#ON SUCCESS returns {"result": "success", "message": "Account created!"}
#ON FAILURE returns {"result": "failure", "message": ...}
def forgetpassword():
    email_recv = request.get_json()['email']
    pass_hash_recv = request.get_json()['password']
    pass_conf = request.get_json()['password2']
    otc_recv = request.get_json()['verificationCode']


    if ((pass_hash_recv or pass_conf) is None):
        resp = flask.make_response({"result": "failure"})
        resp.headers['content_type'] = 'application/json'
        return resp, 400


    #If the pass and pass confirmation do not match
    if (pass_hash_recv != pass_conf):
        resp = flask.make_response({"result": "failure", "message": "Password and Confirm password do not match!"})
        resp.headers['content_type'] = 'application/json'
        return resp, 400

    user = users.query.filter_by(email = email_recv, otc = otc_recv, tmp = 1).all()

    if (not user):
        resp = flask.make_response({"result": "failure", "message":"Please enter the correct one time code or apply for a new one"})
        resp.headers['content_type'] = 'application/json'
        return resp, 400

    user2 = users.query.filter_by(email = email_recv, tmp = 0)

    if (not user2):
        resp = flask.make_response({"result": "failure", "message":"Account with that email does not exist!"})
        resp.headers['content_type'] = 'application/json'
        return resp, 400

    user2[0].pass_hash = pass_hash_recv
    resp = json.dumps({"result": "success", "message": "Your password was successfully changed!"})
    db.session.commit()
    return resp, 200



#The api for update your profile
#METHOD: POST
#Data body: {"email": "mail", "username": "name", "password" :"pass", "password2": "pass", "verificationCode": "code"}
#ON SUCCESS returns {"result": "success", "message": "<message>"}
#ON FAILURE returns {"result": "failure", "message": ...}
def register():
    email_recv = request.get_json()['email']
    username = request.get_json()['username']
    pass_hash_recv = request.get_json()['password']
    pass_conf = request.get_json()['password2']
    otc = request.get_json()['verificationCode']


    if ((pass_hash_recv or pass_conf) is None):
        resp = flask.make_response({"result": "failure"})
        resp.headers['content_type'] = 'application/json'
        return resp, 400


    #If the pass and pass confirmation do not match
    if (pass_hash_recv != pass_conf):
        resp = flask.make_response({"result": "failure", "message": "Password and Confirm password do not match!"})
        resp.headers['content_type'] = 'application/json'
        return resp, 400


    user = users.query.filter_by(email = email_recv, tmp = 1, otc = otc).all()

    #If user has not applied for a one time code
    if (not user):
        resp = flask.make_response({"result": "failure", "message":"Please apply for a one time code first"})
        resp.headers['content_type'] = 'application/json'
        return resp, 400

    user2 = users.query.filter_by(email = email_recv, tmp = 0).all()

    #If user tries to register with an email thats already registered
    if (user2):
        resp = json.dumps({"result": "failure", "message":"User with that email already exists!"})
        return resp, 400

    user2 = users.query.filter_by(username = username, tmp = 0).all()

    #If user tries to register with a username thats already taken
    if (user2):
        resp = json.dumps({"result": "failure", "message":"Username is already taken!"})
        return resp, 400

    #If the user enters an incorrect one time codes
    if (user and (not user[0].tmp or user[0].otc != otc)):
        resp = flask.make_response({"result": "failure", "message":"OTC is incorrect"})
        resp.headers['content_type'] = 'application/json'
        return resp, 400


    #Delete tmp user and create official user account
    if user:
        db.session.delete(user[0])

    #Generates JWT session token
    # JWT_token = genJWT(email_recv).decode()
    JWT_token = genJWT(email_recv)

    critsec.sem.acquire()
    db.session.commit()

    user = users(config.uid, email_recv, pass_hash_recv, None, 0, username, JWT_token, None, None)
    db.session.add(user)
    db.session.commit()
    config.uid += 1

    f = open('var.json', "w")
    json.dump({"uid": config.uid}, f)

    critsec.sem.release()


    resp = json.dumps({"result": "success", "message": "Account created!", "token": JWT_token,"username": username})
    return resp, 200




#The api for generating and sending the one time code to the email. The send code button should link to this
#METHOD: POST
#Data body: {'email': '<your email>'}
#ON SUCCESS returns {"result": "success", "message": "OTC sent!"}
def genotc():
    email_recv = request.get_json()['email']

    #Basic OTC generation
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTC = ""
    length = len(string)

    for i in range(6):
        OTC += string[math.floor(random.random() * length)]

    print(f'\nOTC generated is {OTC}\n')

    #Create temp user
    user = users(config.uid, email_recv, None, OTC, 1, None, None, None, None)
    critsec.sem.acquire()

    config.uid += 1

    f = open('var.json', "w")

    json.dump({"uid": config.uid}, f)

    db.session.add(user)
    db.session.commit()

    critsec.sem.release()

    #Start timer for one time code
    if user:
        t = Timer(20, expire, [user.email, user.otc])
        t.start()

    #Send one time code to email
    sendotc(email_recv, OTC)

    resp = json.dumps({"result": "success", "message": "OTC sent!"})#flask.make_response({"result": "success", "message": "OTC sent!"})
    return resp, 200


'''
request = {
    searchOption: "Movie"(default) or "Director" or "Genre",
    keyword: status=400 if empty or len(keyword) > 40,
    sortOption: "Name ASC" (default) or "Name DESC"or "Rating ASC" or "Rating DESC",
}
ON SUCCESS {json list('ID', 'Name', 'Genre', 'Director', 'Cast', 'Poster', 'Description', 'Rating', 'Year')}
ON FAILURE {"result": "failure", "message": "<message>"}
'''
def search():
    username = request.get_json()['username']

    #Return failure if no keyword is typed
    if not request.get_json()['keyword']:
        resp = json.dumps({"result": "failure", "message": "Please enter keywords to search!"})
        return resp, 400
    else:
        keyword = request.get_json()['keyword']

    #Default values if no input for search or sort options
    if request.get_json()['searchOption'] == '':
        searchOption = 'Movie'
    else:
        searchOption = request.get_json()['searchOption']
    if request.get_json()['sortOption'] == '':
        sortOption = 'Name'
    else:
        sortOption = request.get_json()['sortOption']

    #Return failure if the length of the search term is greater than 40 characters
    if len(keyword) > 40:
        resp = json.dumps({"result": "failure", "message": "The character length should not exceed 40!"})
        return resp, 400
    result = searchFunc(username, keyword, searchOption, sortOption)

    return json.dumps(result)

'''
return the top 10 rating movies
ON SUCCESS {json a list of 10 ('ID', 'Name', 'Genre', 'Director', 'Cast', 'Poster', 'Description', 'Rating')}
ON FAILURE {"result": "failure", "message": "<message>"}
'''
def dashboard():
    username = request.get_json()['username']
    try:
        token = request.get_json()['token']
    except:
        #If the user tries to access the dashboard without a token
        resp = json.dumps({"result": "failure", "message": "Please log in or create an account first"})
        return resp, 400

    if (not token):
        resp = json.dumps({"result": "failure", "message": "Please log in or create an account first"})
        return resp, 400

    #If the user tries to access the dashboard without a valid token
    if (not validate(token)):
        resp = json.dumps({"result": "failure", "message": "Please log in or create an account first"})
        return resp, 400

    #Return dashboard
    result = dashFunc(username)
    return json.dumps(result)


#The api for generating and sending the one time code to the email. The send code button should link to this
#METHOD: POST
#Data body: {'username': '<your username>'}
#ON SUCCESS returns {}
def getwishlist():
    username = request.get_json()['username']
    try:
        result = listwishlist(username)
        return json.dumps(result)
    except:
        resp = json.dumps({"result": "failure", "message": "failed to fetch wishlist"})
        return resp,400


#The api adding a movie to the wishlist
#METHOD: POST
#Data body: {'username': '<your username>'}
#ON SUCCESS returns {"result": "success", "message": "<message>"}
#ON FAILURE returns {"result": "failure", "message": "<message>"}
def addwishlist():
    username = request.get_json()['username']
    movie_id = request.get_json()['movieId']

    id_list = listwishlist(username)

    if id_list == None:
        wishlist_add(username,movie_id)
        resp = json.dumps({"result": "success", "message": "Successfully added!"})
        return resp,200
    else:
        #If movie is already in your wishlist
        if(movie_id in id_list):
            resp = json.dumps({"result": "failure", "message": "You already add this movie in your wishlist!"})
            return resp,400

        #Add movie to wishlist
        wishlist_add(username,movie_id)
        resp = json.dumps({"result": "success", "message": "Successfully added!"})
        return resp,200



#The api removing a movie from the wishlist
#METHOD: POST
#Data body: {'username': '<your username>'}
#ON SUCCESS returns {"result": "success", "message": "<message>"}
#ON FAILURE returns {"result": "failure", "message": "<message>"}
def removewishlist():
    username = request.get_json()['username']
    movie_id = request.get_json()['movieId']

    id_list = listwishlist(username)

    #If a user tries removing a movie that is not in their wishlist
    if (movie_id not in id_list):
        resp = json.dumps({"result": "failure", "message": "This movie is not in your wishlist."})
        return resp,400

    #Removes movie from wishlist
    wishlist_remove(username, movie_id)

    resp = json.dumps({"result": "success", "message": "Successfully removed!"})
    return resp,200


#The api getting all the information of a movie, i.e. rating, genre, director...
#METHOD: POST
#Data body: {'movieId': '<id>'}
#ON SUCCESS returns [[1345836, "name", "genre", "director", "actors", "poster link", "description", rating, year,
                   #[{"rating": rating, "username": "<username>"}]]]
def movieinfo():
    movie_id = request.get_json()['movieId']
    result = movie_info(movie_id)
    return json.dumps(result)


#The api for getting a users wishlist
#METHOD: POST
#Data body: {'username': '<your username>'}
#ON SUCCESS returns [[id, "name", "genre", "Director", "Actors", "<poster link>", "<movie desc>", rating, year,
                   #[{"rating": <rating>, "username": "<your username>"}]]]
def wishlistinfo():
    username = request.get_json()['username']
    result = wishlist_info(username)
    return json.dumps(result)



#The api to check if  a movie is in a users wishlist
#METHOD: POST
#Data body: {'username': '<your username>', 'movieId': 'id'}
#ON SUCCESS returns True
#ON FAILURE returns False
def checkwishlist():
    username = request.get_json()['username']
    movie_id = request.get_json()['movieId']

    id_list = listwishlist(username)

    #If movie is not in wishlist
    if (id_list == None):
        return json.dumps(False)

    #If movie is in wishlist
    elif (movie_id in id_list):
        return json.dumps(True)

    else:
        return json.dumps(False)



#The api to get the rating for a movie
#METHOD: POST
#Data body: {'username': '<your username>', 'movieId': 'id'}
#ON SUCCESS returns <rating>
#ON FAILURE returns {"result": "failure", "message": "fetch failed!"}
def getrating():
    movieId = request.get_json()['movieId']
    username = request.get_json()['username']
    try:
        #Tries to get rating for a movie
        rating = getRating(username, movieId)
        return json.dumps(rating)
    except:
        resp = json.dumps({
            "result": "failure",
            "message": "fetch failed!"})
        return json.dumps(resp), 400



#The api to add the rating for a movie
#METHOD: POST
#Data body: {'username': '<your username>', 'movieId': 'id', 'rating': 'rating'}
#ON SUCCESS returns <"success": "<message>">
#ON FAILURE returns {"result": "failure", "message": "fetch failed!"}
def addrating():
    rating = request.get_json()['rating']
    movieId = request.get_json()['movieId']
    username = request.get_json()['username']

    #Adds rating to movie
    resp, code = addRating(username, rating, movieId)
    return json.dumps(resp), code



#The api to add the review for a movie
#METHOD: POST
#Data body: {'username': '<your username>', 'movieId': 'id', 'content': '<review>'}
#ON SUCCESS returns <"success": "<message>">
#ON FAILURE returns {"result": "failure", "message": "fetch failed!"}
def addreview():
    content = request.get_json()['content']
    movieId = request.get_json()['movieId']
    username = request.get_json()['username']

    # Remove leading and trailing spaces
    content = content.strip()

    #Attaches review to the movie
    resp, code = addMovieReview(username, content, movieId)
    return json.dumps(resp), code




#The api to delete the review for a movie
#METHOD: POST
#Data body: {'username': '<your username>', 'movieId': 'id', 'reviewId': '<id>'}
#ON SUCCESS returns <"success": "<message>">
#ON FAILURE returns {"result": "failure", "message": "fetch failed!"}
def deletereview():
    reviewId = request.get_json()['reviewId']
    movieId = request.get_json()['movieId']
    username = request.get_json()['username']

    #Delets review from movie
    resp, code = deleteReview(username, reviewId, movieId)
    return json.dumps(resp), code



#The api to get the review for a movie for the movie information page
#METHOD: POST
#Data body: {'username': '<your username>', 'movieId': 'id'}
#ON SUCCESS returns <"success": "<message>">
#ON FAILURE returns {"result": "failure", "message": "fetch failed!"}
def getmoviereview():
    movieId = request.get_json()['movieId']
    username = request.get_json()['username']

    try:
        #Tries to get the review for a movie
        reviewList = getMovieReview(username, movieId)
        return json.dumps(reviewList)
    except:
        resp = json.dumps({
            "result": "failure",
            "message": "fetch failed!"})
        return json.dumps(resp), 400


#The api to get the users review for a movie in the profile page
#METHOD: POST
#Data body: {'username': '<your username>'}
#ON SUCCESS returns <"success": "<message>">
#ON FAILURE returns {"result": "failure", "message": "fetch failed!"}
def getuserreview():
    username = request.get_json()['username']
    try:
        #Tries to get the users reviews for the profile page
        reveiwList = getUserReview(username)
        return json.dumps(reveiwList)
    except:
        resp = json.dumps({
            "result": "failure",
            "message": "fetch failed!"})
        return json.dumps(resp), 400



#The api to get the banlist for a user
#METHOD: POST
#Data body: {'username': '<your username>'}
#ON SUCCESS returns <"success": "<message>">
#ON FAILURE returns {"result": "failure", "message": "failed to fetch banlist"}
def getbanlist():
    username = request.get_json()['username']

    try:
        #Tries to get the banlist for a user
        result = listbanlist(username)
        return json.dumps(result)
    except:
        resp = json.dumps({"result": "failure", "message": "failed to fetch banlist"})
        return resp,400



#The api to add a user to the banlist for a user
#METHOD: POST
#Data body: {'username': '<your username>', 'ban_name': '<user you want to ban>'}
#ON SUCCESS returns <"success": "<message>">
#ON FAILURE returns {"result": "failure", "message": "<message>"}
def addbanlist():
    username = request.get_json()['username']
    ban_name = request.get_json()['ban_name']

    #Gets the banlist for a user
    banlist = listbanlist(username)

    #If the banlist does not already contain the user to be added
    if banlist == []:
        banlist_add(username,ban_name)
        resp = json.dumps({"result": "success", "message": "Successfully added!"})
        return resp,200

    else:
        #If the banlist does already contain the user to be added
        if(ban_name in banlist):
            resp = json.dumps({"result": "failure", "message": "You already add this user in your banlist!"})
            return resp,400

        #Adds user to banlist
        banlist_add(username,ban_name)
        resp = json.dumps({"result": "success", "message": "Successfully added!"})
        return resp,200


#The api to remove a user from the banlist for a user
#METHOD: POST
#Data body: {'username': '<your username>', 'ban_name': '<user you want to unban>'}
#ON SUCCESS returns <"success": "<message>">
#ON FAILURE returns {"result": "failure", "message": "<message>"}
def removebanlist():
    username = request.get_json()['username']
    ban_name = request.get_json()['ban_name']

    #Get the banlist for the user performing the action
    banlist = listbanlist(username)

    #If user tries to remove a user from a banlist that was never banned
    if (ban_name not in banlist):
        resp = json.dumps({"result": "failure", "message": "This user is not on your banlist."})
        return resp,400

    #Removes user from banlist
    banlist_remove(username, ban_name)
    resp = json.dumps({"result": "success", "message": "Successfully removed!"})
    return resp,200



#The api to get a users rating for a movie
#METHOD: POST
#Data body: {'username': '<your username>', 'movieId': '<id>'}
#ON SUCCESS returns <'rating': rating>
def getuserrating():
    username = request.get_json()['username']
    movieId = request.get_json()['movieId']

    #Fetches users rating for a movie
    rating = getUserRating(username, movieId)
    return json.dumps(rating)



#The api to check if a user is in the banlist of another user
#METHOD: POST
#Data body: {'username': '<your username>', 'ban_name': '<user you want to check>'}
#ON SUCCESS returns True
#ON FAILURE returns False
def checkbanlist():
    username = request.get_json()['username']
    ban_name = request.get_json()['ban_name']

    #Get users banlist
    banlist = listbanlist(username)

    #If banlist is empty
    if (banlist == None):
        return json.dumps(False)

    #If user exists in the banlist
    elif (ban_name in banlist):
        return json.dumps(True)
    else:
        return json.dumps(False)

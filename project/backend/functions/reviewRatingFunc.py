from statistics import mean
import psycopg2;
from psycopg2.extras import Json
import sys
sys.path.append('../')
from functions.banlist import listbanlist
from machine.sentiment import sentiment_analysis
from machine.spam import *
'''
movie review structure (array of JSON dict)
Json({
    "username": username,
    "movieId": movieId,
    "rating": rating,
    "reviewId": reviewId,
    "content": content,
    "sentimentAnalysis": None, # TODO: put sentimentAnalysis fucntion here
    "spam": None, # TODO: put spam fucntion here
    "similarityScore": None, #TODO: put similarityScore fucntion here
})
'''
# Add review and related information to the movie review database
def addMovieReview(username, content, movieId):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()
    cur.execute('''select name from "MovieFinder" where id={}'''.format(movieId))
    movieName = cur.fetchall()[0][0]

    # Check if there is rating for username in movieId
    cur.execute('''select ratings from "MovieFinder" where id={}'''.format(movieId))
    ratings = cur.fetchall()[0][0]

    if (not ratings):
        resp = {"result": "failure", "message": "Please rate the movie first!"}
        return resp, 400

    index = next((index for (index, ratings) in enumerate(ratings)
          if ratings["username"] == username), None)

    if index == None:
        resp = {"result": "failure", "message": "Please rate the movie first!"}
        return resp, 400

    rating = ratings[index]["rating"]

    # Get review list
    cur.execute('''select review from "MovieFinder" where id={}'''.format(movieId))
    reviewList = cur.fetchall()[0][0]

    if not reviewList:
        reviewId = 1
        reviewList = list()
    else:
        prevReview = reviewList[0]
        prevReviewStr = prevReview["username"] + str(prevReview["movieId"])
        reviewId = str(int(prevReview["reviewId"][len(prevReviewStr):])+1)

    reviewId = username+str(movieId)+str(reviewId)
    sentimentscore = sentiment_analysis(content)
    movieReview = Json({
                "username": username,
                "movieId": movieId,
                "rating": rating,
                "reviewId": reviewId,
                "content": content,
                "sentimentAnalysis": sentimentscore,
                "spam": spam(content),
                "similarityScore": None,
            })
    # Update the review in movie database if the content is not empty
    if (content.strip() != ''):
        cur.execute('''update "MovieFinder" set review=({}::jsonb || review) where id='{}' '''
                        .format(movieReview, movieId))
        conn.commit()

        # Update user review
        userReview = Json({
            "movieId": movieId,
            "reviewId": reviewId,
            "movieName": movieName,
            "content": content
        })

        cur.execute('''update "users" set review=({}::jsonb || review) where username='{}' '''
                    .format(userReview, username))
        conn.commit()
        cur.close()
        conn.close()

        resp = {"result": "success", "message": "Review has been successfully added!"}
        return resp, 200

# Get the movie review list for each user (considered the banlist)
def getMovieReview(username, movieId):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()
    cur.execute('''select review from "MovieFinder" where id='{}' '''.format(movieId))
    reviewList = cur.fetchall()[0][0]

    banlist = listbanlist(username)
    result = []

    if not reviewList:
        return []

    if not banlist:
        return reviewList

    for review in reviewList:
        if review['username'] not in banlist:
            result.append(review)

    return result

# Add rating to movie & user review;
def addRating(username, rating, movieId):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    # Update the movie rating list
    movieRating = Json({
        "username":username,
        "rating": rating,
        })
    cur.execute('''select ratings from "MovieFinder" where id={}'''.format(movieId))
    ratingList = cur.fetchall()[0][0]

    if not getRatingList(movieId):
        cur.execute('''update "MovieFinder" set ratings=array[{}]::jsonb[] where id='{}' '''
                    .format(movieRating, movieId))

    elif next((rating for rating in ratingList if rating["username"]==username), None):
        resp = {"result": "failure", "message": "You can only rate once!"}
        return resp, 400

    else:
        cur.execute('''update "MovieFinder" set ratings=({}::jsonb || ratings)  where id='{}' '''
                    .format(movieRating, movieId))

    conn.commit()

    # Update the movie average rating
    cur.execute('''select ratings from "MovieFinder" where id='{}' '''.format(movieId))
    reviewList = cur.fetchall()[0][0]

    cur.execute('''update "MovieFinder" set rating={} where id={} '''
                .format(calAvgRating(reviewList), movieId))
    conn.commit()
    # Get the movie name, which the user rated
    cur.close()
    conn.close()

    resp = {"result": "success", "message": "Rating has been successfully sent!"}
    return resp, 200

# Delete review in movie and user database
def deleteReview(username, reviewId, movieId):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    # Delete the review in movie review
    cur.execute('''select review from "MovieFinder" where id={}'''.format(movieId))
    reviewList = cur.fetchall()[0][0]

    index = next((index for (index, review) in enumerate(reviewList)
          if review["reviewId"] == reviewId), None)

    cur.execute('''update "MovieFinder" set review=array_remove(review, review[{}]) where id={}'''
                .format(index+1, movieId))
    conn.commit()

    # Change the content in user review
    cur.execute('''select review from "users" where username='{}' '''.format(username))
    reviewList = cur.fetchall()[0][0]
    index = next((index for (index, review) in enumerate(reviewList)
          if review["reviewId"] == reviewId), None)

    cur.execute('''update "users" set review=array_remove(review, review[{}]) where username='{}' '''
                .format(index+1, username))
    conn.commit()
    cur.close()
    conn.close()

    resp = {"result": "success", "message": "This review has been successfully deleted!"}
    return resp, 200

# Get reviews from the user profile
def getUserReview(username):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()
    cur.execute('''select review from "users" where username='{}' '''.format(username))

    review = cur.fetchall()[0][0]
    if not review:
        return []

    return review

# Calculate the average rating based on given list of dictionaries
def calAvgRating(ratingList):
    ratings = [review['rating'] for review in ratingList]

    if not ratings or len(ratings) == 0:
        return 0.0
    return round(mean(ratings),1)

# Get the rating for each user (considered banlist)
'''
ratings [{
    "username": String,
    "rating": double/float,
}]
'''
def getRating(username, movieId):
    ratinglist = getRatingList(movieId)
    result = []
    banlist = listbanlist(username)

    if not ratinglist or not banlist:
        return calAvgRating(ratinglist)

    for rate in ratinglist:
        if rate['username'] not in banlist:
            result.append(rate)

    return calAvgRating(result)

# Get the ratings list for each movie
'''
ratings [{
    "username": String,
    "rating": int,
},]
'''
def getRatingList(movieId):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()
    cur.execute('''select ratings from "MovieFinder" where id={}'''.format(movieId))

    ratings = cur.fetchall()[0][0]
    if not ratings:
        return []

    cur.close()
    conn.close()

    return ratings

# TEST function to get the general mean rating
def getGeneralRating(movieId):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    cur.execute('''select rating from "MovieFinder" where id={}'''.format(movieId))
    rating = cur.fetchall()[0][0]
    cur.close()
    conn.close()

    return rating

# Get all general moview review for each movie
def getGeneralMovieReview(movieId):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    cur.execute('''select review from "MovieFinder" where id={}'''.format(movieId))
    review = cur.fetchall()[0][0]

    cur.close()
    conn.close()

    return review

# Get single user rating for given movieId
def getUserRating(username, movieId):
    ratings = getRatingList(movieId)
    if not ratings or ratings == []:
        return 0

    ratingDict = next((rating for rating in ratings if rating["username"] == username), None)
    if not ratingDict:
        return None

    return ratingDict["rating"]

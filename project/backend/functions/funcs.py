import psycopg2
import sys
sys.path.append('../')
from backend.functions.reviewRatingFunc import getRating;

# Search by keyword, search options, return the movie information list sorted by sort option
def searchFunc(username, keyword, searchOption, sortOption):
    # Set up the postgreSQL connections
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    # Convert the Name to Movie in searchOption
    if searchOption == "Movie":
        searchOption = "name"

    # Define the sort option orders
    if sortOption == "Name ASC":
        # sortOption = ["name ASC", "rating ASC"]
        sortOption = {"sort1":1, "sort2":7, "reverse":False}

    elif sortOption == "Name DESC":
        # sortOption = ["name DESC", "rating ASC"]
        sortOption = {"sort1":1, "sort2":7, "reverse":True}

    elif sortOption == "Rating ASC":
        # sortOption = ["rating ASC", "name ASC"]
        sortOption = {"sort1":7, "sort2":1, "reverse":False}

    elif sortOption == "Rating DESC":
        # sortOption = ["rating DESC", "name ASC"]
        sortOption = {"sort1":7, "sort2":1, "reverse":True}

    # Execute search in postgreSQL database
    cur.execute('''select * from "MovieFinder" where {} ilike '%{}%' '''.format(searchOption, keyword))
    infoList = cur.fetchall()

    # Close connections and return the result
    cur.close()
    conn.close()

    # keys for infoList ('ID', 'Name', 'Genre', 'Director', 'Cast', 'Poster', 'Description', 'Rating')
    for i in range(len(infoList)):
        infoList[i] = list(infoList[i])
        infoList[i][7] = getRating(username, infoList[i][0])


    infoList.sort(key=lambda info: (info[sortOption['sort1']]), reverse=sortOption['reverse'])
    # keys = ('ID', 'Name', 'Genre', 'Director', 'Cast', 'Poster', 'Description', 'Rating')
    return infoList

# Return the 10 highest rating movie information list to home website based on username
def dashFunc(username):
    # Set up the postgreSQL connections
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    # Execute search in postgreSQL database
    cur.execute('''select * from "MovieFinder" order by CAST(rating as double precision) DESC limit 50''')
    infoList = cur.fetchall()

    for i in range(len(infoList)):
        infoList[i] = list(infoList[i])
        infoList[i][7] = getRating(username, infoList[i][0])

    infoList.sort(key=lambda info: (info[7]), reverse=True)

    # Close connections and return the result
    cur.close()
    conn.close()
    return infoList[:10]

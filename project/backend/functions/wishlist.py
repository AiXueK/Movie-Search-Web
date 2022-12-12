import psycopg2;
from functions.reviewRatingFunc import *

'''
return a list of movieId about all movie in wishlist
'''
def listwishlist(username):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    cur.execute('''select wishlist from "users" where username = '{}' '''.format(username))
    result = cur.fetchall()
    cur.close()
    conn.close()

    if result == []:
        return []

    #because database will return a value like "[(123,)]"
    [(result,)] = result

    if result == '' or result == None:
        return []

    result = result.split(',')
    return result

'''
enter a movieid and return all information about this movie
'''
def movie_info(movieid):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    cur.execute('''select * from "MovieFinder" where ID = {}'''.format(movieid))
    result = cur.fetchall()
    cur.close()
    conn.close()

    return result

'''
add a movie to wishlist
'''
def wishlist_add(username, movieid):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()
    result = listwishlist(username)

    #if wishlist is empty
    if result == []:
        cur.execute('''update users set wishlist = '{}' where username = '{}' '''.format(movieid, username))
        conn.commit()
        cur.close()
        conn.close()
        return

    result.append(movieid)

    #change the list to a string so that it can be stored in database.
    result = ",".join([str(x) for x in result])
    cur.execute('''update users set wishlist = '{}' where username = '{}' '''.format(result, username))
    conn.commit()
    cur.close()
    conn.close()

    return

'''
remove a movie from wishlist
'''
def wishlist_remove(username, movieid):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    wishlist = listwishlist(username)
    wishlist.remove(movieid)

    if wishlist == []:
        cur.execute('''update users set wishlist = null where username = '{}' '''.format(username))
        conn.commit()
        cur.close()
        conn.close()
        return

    #change the list to a string so that it can be store in database.
    wishlist = ",".join([str(x) for x in wishlist])
    cur.execute('''update users set wishlist = '{}' where username = '{}' '''.format(wishlist, username))
    conn.commit()
    cur.close()
    conn.close()

    return

'''
return a list of list which contain all movie information in wishlist
'''
def wishlist_info(username):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    wishlist = listwishlist(username)
    movie_info_list = []

    #if wishlist is empty
    if (wishlist is []):
        return []

    # do a loop to make the movie information in the wishlist table to a list of list
    for movie in wishlist:
        if (not len(movie) or movie == '{}'):
            continue

        cur.execute('''select * from "MovieFinder" where id = '{}' '''.format(movie))
        info = cur.fetchall()

        #recalculate the rating because the user's rating will not be seen by the user who added him to banlist
        rate = getRating(username, movie)
        info[0] = list(info[0])
        info[0][7] = rate
        movie_info_list.append(info[0])

    cur.close()
    conn.close()

    return movie_info_list

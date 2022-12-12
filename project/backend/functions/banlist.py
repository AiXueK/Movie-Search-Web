import psycopg2;

'''
enter a username and return a list of Id about all user in banlist
'''
def listbanlist(username):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    cur.execute('''select banlist from "users" where username = '{}' '''.format(username))
    result = cur.fetchall()
    cur.close()
    conn.close()
    if result == []:
        return []

    #because database will return a value like "[(123,)]"
    [(result,)] = result
    if result == None or result == '':
        return []
    result = result.split(',')
    return result

'''
add a user to banlist
'''
def banlist_add(username, ban_name):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    result = listbanlist(username)

    #if banlist is empty
    if result == []:
        cur.execute('''update users set banlist = '{}' where username = '{}' '''.format(ban_name, username))
        conn.commit()
        cur.close()
        conn.close()
        return

    result.append(ban_name)

    #change the list to a string so that it can be store in database.
    result = ",".join([str(x) for x in result])
    cur.execute('''update users set banlist = '{}' where username = '{}' '''.format(result, username))
    conn.commit()
    cur.close()
    conn.close()

    return

'''
remove a user from banlist
'''
def banlist_remove(username, ban_name):
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()

    banlist = listbanlist(username)
    banlist.remove(ban_name)

    #if banlist is empty
    if banlist == []:
        cur.execute('''update users set banlist = null where username = '{}' '''.format(username))
        conn.commit()
        cur.close()
        conn.close()
        return

    #change the list to a string so that it can be store in database.
    banlist = ",".join([str(x) for x in banlist])
    cur.execute('''update users set banlist = '{}' where username = '{}' '''.format(banlist, username))
    conn.commit()
    cur.close()
    conn.close()

    return

'''
The max amount of characters that can be entered is 40
The backend will do a query that will match any movie that contants the characters input
The dropdown list is sorted by name by default
A dropdown list allowing user to choose whether they want to search by director or movie name.  
'''
import psycopg2;
import json

def searchFunc(keyword, searchOption, sortOption):
    # Set up the postgreSQL connections
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()
    
    # Convert the Name to Movie in searchOption
    if searchOption == "Movie":
        searchOption = "Name"
        
    # Define the sort option orders
    if sortOption == "Name":
        sortOption = ["Name", "Rating"]
    elif sortOption == "Rating":
        sortOption = ["Rating", "Name"]
    
    # Execute search in postgreSQL database
    sql = '''select * from "MovieFinder" where {} ilike %(keyword)s order by {}, {}'''.format(searchOption, sortOption[0], sortOption[1])
    cur.execute(sql, {'keyword': '%{}%'.format(keyword)})
    result = cur.fetchall()
    # Close connections and return the result
    cur.close()
    conn.close()
            
    return result

def dashFunc():
    # Set up the postgreSQL connections
    conn = psycopg2.connect(host="127.0.0.1", port="5432",database="MovieFinder", user="postgres", password="admin")
    cur = conn.cursor()
    
    sortOption = ["Rating", "Name"]
    # Execute search in postgreSQL database
    cur.execute('''select * from "MovieFinder" order by {}, {} limit 10'''.format(sortOption[0], sortOption[1]))
    result = cur.fetchall()

    # Close connections and return the result
    cur.close()
    conn.close()
    return result
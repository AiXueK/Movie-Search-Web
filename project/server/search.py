import psycopg2;


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
    # cur.execute('''select * from "MovieFinder" where Name ilike %(value)s order by Name, Rating''', {'value': '%{}%'.format(value)})

    value = "almost"
    # cur.execute('''select * from "MovieFinder" where {} ilike '%{}%' order by {}, {}'''.format(searchOption, keyword, sortOption[0], sortOption[1]))
    sql = '''select * from "MovieFinder" where {} ilike %(keyword)s order by {}, {}'''.format(searchOption, sortOption[0], sortOption[1])

    cur.execute(sql, {'keyword': '%{}%'.format(keyword)})
    result = cur.fetchall()
    # Close connections and return the result
    cur.close()
    conn.close()
    
    # Convert list to dict
    keys = ('ID', 'Name', 'Genre', 'Director', 'Cast', 'Poster', 'Description', 'Rating', 'Year')
    # print(result)
    movieDict = {
        'ID': [],
        'Name': [],
        'Genre': [],
        'Director': [],
        'Cast': [],
        'Poster': [],
        'Description': [],
        'Rating': [],
        'Year': [],
    }

    for element in result:
        for index in range(0, len(keys)):
            movieDict[keys[index]].append(element[index])
    print(movieDict)
    return result

searchFunc('almost', 'Movie', 'Name')
import os
from json import dumps
import json
from flask import Flask, request, Response
from flask_cors import CORS
from funcs import searchFunc, dashFunc

def defaultHandler(err):
	response = err.get_response()
	print('response', err, err.get_response())
	response.data = dumps({
		"code": err.code,
		"name": "System Error",
		"message": err.get_description(),
	})
	response.content_type = 'application/json'
	return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# baseURL = 'http://localhost:5000/'

# http://localhost:5000?keyword=Bana&searchOption=Movie&sortOption=Name
'''
request = {
    searchOption: "Movie"(default) or "Director" or "Genre",
    keyword: status=400 if empty or len(keyword) > 40,
    sortOption: "Name" (default) or "Rating",
}
response = {json list('ID', 'Name', 'Genre', 'Director', 'Cast', 'Poster', 'Description', 'Rating', 'Year')}
'''
url = 'http://localhost:5000/search'
@APP.route('/search', methods=['POST'])
def search():
    if not request.get_json()['keyword']:
        return Response(
            "Please enter a keyword to search",
            status=400,
        )
    else:
        keyword = request.get_json()['keyword']
    # Default values if no input for search or sort options
    if request.get_json()['searchOption'] == '':
        searchOption = 'Movie'
    else:
        searchOption = request.get_json()['searchOption']
    if request.get_json()['sortOption'] == '':
        sortOption = 'Name'
    else:
        sortOption = request.get_json()['sortOption'] 

    if len(keyword) > 40:
        return Response(
        "Input exceeds 40 characters",
        status=400,
        )
    result = searchFunc(keyword, searchOption, sortOption)
    
    return json.dumps(result)   

'''
return the top 10 rating movies
response = {json a list of 10 ('ID', 'Name', 'Genre', 'Director', 'Cast', 'Poster', 'Description', 'Rating', 'Year')}
'''
@APP.route('/home', methods=['GET'])
def dashboard():
    result = dashFunc()
    return json.dumps(result)   

if __name__ == '__main__':
    APP.run(debug=True, port=5000)
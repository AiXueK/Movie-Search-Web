import sys
sys.path.append('/functions')
import nltk
import database
from flask_cors import CORS
import json
from routes import webroutes

def defaultHandler(err):
	response = err.get_response()
	print('response', err, err.get_response())
	response.data = json.dumps({
		"code": err.code,
		"name": "System Error",
		"message": err.get_description(),
	})
	response.content_type = 'application/json'
	return response


#import variables from database.py
app = database.app
db = database.db

CORS(app)

app.config['TRAP_HTTP_EXCEPTIONS'] = True

if __name__ == "__main__":
    nltk.download('stopwords')
    nltk.download('vader_lexicon')
    app.run(debug=False)

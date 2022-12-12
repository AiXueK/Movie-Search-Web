import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from database import users


JWT_KEY = "Sigma Rule 01" #JWT key used to sign auth tokens

user = users.query.filter_by().order_by(users.uid.desc()).first()

#Gets the lowest uid available in the database
if (not user) :
    uid = 0
else :
    uid = user.uid + 1

#Loads movies csv file
metadata = pd.read_csv('../movies_initial.csv', low_memory=False).drop_duplicates(subset='id', keep="first").reset_index()

tfidf = TfidfVectorizer(stop_words='english')

metadata['description'] = metadata['description'].fillna('')

tfidf_matrix = tfidf.fit_transform(metadata['description'])

#Machine learning model to get the matrix of similar movies
cosine_sim2 = linear_kernel(tfidf_matrix, tfidf_matrix)

#Construct a reverse map of indices and movie titles
indices = pd.Series(metadata.index, index=metadata['id'])#.drop_duplicates()

# import sys
# sys.path.append('.')
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
import psycopg2
def spam(review):
    df1 = pd.read_csv("machine/Sigma-Channel1.csv")
    df2 = pd.read_csv("machine/Sigma-Channel2.csv")
    df3 = pd.read_csv("machine/Sigma-Channel3.csv")
    df4 = pd.read_csv("machine/Sigma-Channel4.csv")
    df5 = pd.read_csv("machine/Sigma-Channel5.csv")

    frames = [df1, df2, df3, df4, df5]
    # create a single data frame
    df_merged = pd.concat(frames)

    # assigning keys to allow model know the respective database
    keys = ["Channel1","Channel2","Channel3","Channel4","Channel5"]
    df_with_keys = pd.concat(frames,keys=keys)

    df = df_with_keys
    # extracting columns from database
    df_data = df[["CONTENT","CLASS"]]

    df_x = df_data['CONTENT']
    df_y = df_data['CLASS']

    corpus = df_x
    # raw texts are converted to vector numeric values. Preparing to fit in
    # machine learning model
    cv = CountVectorizer()
    X = cv.fit_transform(corpus)
    # Algorithm will use 70% of data for training model, 30% will be used for model testing.
    X_train, X_test, y_train, y_test = train_test_split(X, df_y, test_size=0.30, random_state=42)
    # Naive Bayes algorithm to train the spam model
    clf = MultinomialNB()
    # fitting model into dataset to identify pattterns and insights of the dataset
    clf.fit(X_train,y_train)

    comment = ["{}".format(review)]
    test_score = clf.score(X_train, y_train) * 100
    print(f"Accuracy = {test_score:.2f}%")
    # converting result into array
    vect = cv.transform(comment).toarray()
    result = clf.predict(vect)

    if (result[0] == 1):
        return True

    return False

import re
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def sentiment_analysis(content):
    #download stopwords from nltk
    stopword = set(stopwords.words('english'))
    # add some punctuation to stopword
    for w in ['!',',','.','?','-s','-ly','</s>','s']:
        stopword.add(w)
    #remove not from stopword because not will convert many words to antonyms, it should not be used as stopword
    stopword.remove('not')
    #Lowercase the review, delete stopwords, etc. to improve the accuracy of the analysis
    content = str(content).lower()
    content = re.sub(r'[^a-zA-Z ]+', '', content)
    content = re.sub('\n', '', content)
    content = [word for word in content.split(' ')if word not in stopword]
    content = ' '.join(content)
    #calculate the polarity scores
    scores = SentimentIntensityAnalyzer().polarity_scores(content)
    #1 for positive,-1 for negative and 0 for neutral
    if scores['pos']> scores['neu'] and scores['pos']> scores['neg']:
        return 1
    elif scores['neg']> scores['pos'] and scores['neg']> scores['neu']:
        return -1
    else:
        return 0
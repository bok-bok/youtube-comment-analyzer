import re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer



def sentiment(data):
    data = preprocess(data)
    data = sentiment_helper(data)
    return data 

def sentiment_helper(data):
    def classify(score):
        if score > 0:
            return 'Positive'
        elif score < 0:
            return 'Negative'
        else:
            return 'Neutral'
    sia = SentimentIntensityAnalyzer()
    data['sentiment score'] = data['pre_comments'].map(lambda x : sia.polarity_scores(x)['compound'])
    data['sentiment category'] = data['sentiment score'].map(classify)
    data.drop('pre_comments', axis= 1, inplace = True)
    #data.drop('token', axis = 1, inplace = True)
    return data
    

def preprocess(data):
    data['pre_comments'] = data['comments'].str.replace("[^a-zA-Z#]", " ", regex=True)
    data['pre_comments'] = data['pre_comments'].map(lambda x : ' '.join([w for w in x.split() if len(w) > 3]))
    data['pre_comments'] = data['pre_comments'].map(str.lower)

    #token = data['pre_comments']
    
    #wnl = WordNetLemmatizer()
    #token = token.map(lambda x : [wnl.lemmatize(i) for i in x if i not in set(stopwords.words('english'))])
    #token = token.map(lambda x : ' '.join(x))
    #data['token'] = token
    return data
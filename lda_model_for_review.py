# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:16:26 2017

@author: 30216
"""
import sys
sys.path.append("C:\Python27\Lib\site-packages")
from nltk.tokenize import RegexpTokenizer
#from stop_words import get_stop_words
#from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from gensim import corpora, models
import numpy as np
import pandas as pd
import gensim
#import random
import re

class TopicModelling(object):

    def strCleaner(self, fullData):
    
        raw_text = " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(\d+)|(\b\w{1,2}\b)", " ", fullData).split())
        text = raw_text.replace(" 39 ","").replace("quot","")
        return text.encode('utf-8')
    
    def review_wise_topic(self, review):
    
        texts = []
        tokenizer = RegexpTokenizer(r'\w+')

        # create English stop words list
        #en_stop = get_stop_words('en')
        #stop = set(stopwords.words('english'))
        stop_word = []
        f = open("stop_words.txt","r")
        stop_word = f.read()

        # creating lemmatization word list
        lemma = WordNetLemmatizer()
    
        raw = review.lower()
        raw_text = self.strCleaner(raw)
        tokens = tokenizer.tokenize(raw_text)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in stop_word]

        # stem token
        stemmed_tokens = [lemma.lemmatize(i) for i in stopped_tokens]
       
        # add tokens to list
        texts.append(stemmed_tokens)
        
        dictionary = corpora.Dictionary(texts)

        # convert tokenized documents into a document-term matrix
        corpus = [dictionary.doc2bow(text) for text in texts]

        # generate LDA model
        np.random.seed(1000)

        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)

        #print(ldamodel.print_topics(num_topics=1, num_words=3))
        rev_topics = ldamodel.print_topics(num_topics=1, num_words=6)
        
        return rev_topics[0]

    def review_topic(self, query):
  
    
        topics = []
        
        review_text = query['Review']
        
        for i in range(0,len(review_text)):
        
            parsed_review = {}
            parsed_review['review'] = review_text[i]        
            parsed_review['topic'] = self.review_wise_topic(review_text[i])
            topics.append(parsed_review)
        return topics
        

final = "Reviews"+","+"Topics"
print final.decode('ascii','ignore')

def main():
    
    rev = TopicModelling()    
    reviews = pd.read_csv("D:\\POC\\Vision 2017\\Review website\\aviva.csv")
    reviews.columns = reviews.columns.str.strip()
    revtopic = rev.review_topic(query = reviews)
    topics = pd.DataFrame(revtopic)
    
    for i in range(0,len(reviews)):
        try:
            #tweet = str(twitter_data['twt_text'][i])
            review = str(reviews['Review'][i])
            topic = str(topics['topic'][i])
            final_data = review+","+topic
            print final_data.decode('ascii','ignore')
        
        except Exception ,e:
            pass
    

if __name__ == "__main__":
    # calling main function
    main()
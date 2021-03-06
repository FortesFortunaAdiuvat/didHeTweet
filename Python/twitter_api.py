from twython import Twython
import time
from os import path
from scipy.misc import imread
import numpy as np
import matplotlib.pyplot as plt
import random
from palettable.colorbrewer.sequential import Blues_9, YlGnBu_9
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
#APP_KEY = ''
#APP_SECRET = ''
#twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
#ACCESS_TOKEN = twitter.obtain_access_token()
#twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

def last_trump_time(twitter):
    created=twitter.get_user_timeline(screen_name="realdonaldtrump", count=1)[0]['created_at']
    creation_time=time.strptime(created, "%a %b %d %H:%M:%S %z %Y")
    timediff=(time.time()-time.mktime(creation_time))/60
    return('{{"time": "{}", "in_five_min": "{}", "in_ten_min": "{}", "last_hour":"{}","today":"{}"}}'.
        format(created,str(timediff<5),str(timediff<10),str(timediff<60),str(timediff<1440)))

def get_trump_count(twitter):
    return twitter.show_user(screen_name="realdonaldtrump")["statuses_count"]
    
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return tuple(YlGnBu_9.colors[random.randint(2,8)])
    
def trump_wc(twitter):    
    d = path.dirname(__file__)   
    tweets=twitter.get_user_timeline(screen_name="realdonaldtrump", count=20000)
    tweets=" ".join([tweet['text'] for tweet in tweets])
    tweets = " ".join([word for word in tweets.split()
                            if 'http' not in word
                                and not word.startswith('@')
                                and word != 'RT'
                            ])
    trump_mask = imread(path.join(d, "wh1.png"), flatten=True)
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="black", max_words=2000, mask=trump_mask, 
                   stopwords=stopwords)
    # generate word cloud
    wc.generate(tweets) 
    wc.recolor(color_func=color_func, random_state=3)
    # store to file
    wc.to_file(path.join(d, "trump_wc.png"))
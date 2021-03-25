import tweepy
import spacy
from .models import DB, User

auth = tweepy.OAuthHandler("NMV0tKMlshhMYTzqwh44CjPzV",
                           "QhLLsomQrqvfGiPb8pCemrKND7izBWLf2Vkuzf1xTjA1pzsFtu")
twitter = tweepy.API(auth)

nlp = spacy.load("my_model")


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def get_info_and_add(username):
    try:
        twitter_user = twitter.get_user(username)
        tweets = twitter_user.timeline(
            count=500,
            exclude_replies=True,
            include_rts=False
        )
        tweets_text = []
        embeddings = []
        for tweet in tweets:
            tweets_text.append(tweet.text)
            tweet_vector = vectorize_tweet(tweet.text)
            embeddings.append(tweet_vector)

        DB_user = User(
            id=twitter_user.id,
            username=twitter_user.name,
            fullname=twitter_user.name,
            tweets=tweets_text,
            embeddings=embeddings
        )
        DB.session.add(DB_user)
        DB.session.commit()

        return DB_user

    except Exception as e:
        print("Error Processing %s: %s" % (username, e))

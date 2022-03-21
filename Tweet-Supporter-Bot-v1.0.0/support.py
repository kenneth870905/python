#-----------important-------------
import tweepy
import logging
#--------------varibales----------
#set logger
logging.basicConfig(
    filename="app.log",
    format = "%(levelname)s - %(asctime)s - %(name)s : %(message)s ", 
    datefmt="%Y-%m-%d %k:%M:%S"
)
logger = logging.getLogger("TweetBot[Stream]")
#--------------Body---------------
class StreamNewTweets(tweepy.Stream):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, reply_content : str, target_list : list):
        #set custom fields
        self.reply_content = reply_content
        self.target_list = target_list
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret)

    def on_status(self, status : tweepy.models.Status):
        #receive new statuses

        #ignore replies
        if (status.in_reply_to_status_id is not None):
            return
        #ignore tweeted by other users
        if (not status.user.id_str in self.target_list):
            return
        #call support function
        self.support_tweet(status)
    
    def on_error(self, error):
        logger.error(error)

    def support_tweet(self, tweet : tweepy.models.Status):
        #fav
        if not tweet.favorited:
            try:
                tweet.favorite()
            except:
                logger.error("error to fav")
        #retweet
        if not tweet.retweeted:
            try:
                tweet.retweet()
            except:
                logger.error("error to retweet")
        #reply (comment)
        try:
            self.api.update_status(self.reply_content, tweet.id) 
        except:
            logger.error("error to send reply")
        #bookmark
        #bookmark option is not exists in twitter api for developers

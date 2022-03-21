#-----------important-------------
import tweepy
import json
import logging
from random import choice
from pyfiglet import figlet_format


from support import StreamNewTweets
from config import *
#----------variables----------
#set logger
logging.basicConfig(
    filename="app.log",
    format = "%(levelname)s - %(asctime)s - %(name)s : %(message)s ",
    datefmt="%Y-%m-%d %k:%M:%S"
)
logger = logging.getLogger("Tweet-Bot[Main]")
#-------------Body----------------
def get_api_list():
    _api_list = []
    #read api list from file
    try:
        with open(api_list_filename, "r") as file:
            api_list = file.read().split('\n')
    except:
        return _api_list
    #convert to a list of dictionary
    for api in api_list:
        #specific format ::: 
        api = api.split(":")
        if len(api) == 4:
            api = {
                "consumer_key" : api[0],
                "consumer_secret": api[1],
                "access_token" : api[2],
                "access_token_secret" : api[3],
            }
            _api_list.append(api)
    return _api_list

def get_reply_content():
    reply_content = None
    try:
        with open(text_filename, 'r', encoding='utf8') as file:
            reply_content = file.read()
    except:
        pass
    finally:
        return reply_content

def create_api(api_info):
    #authorize client
    auth = tweepy.OAuthHandler(api_info['consumer_key'], api_info['consumer_secret'])
    auth.set_access_token(api_info['access_token'], api_info['access_token_secret'])
    #authorazition
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("can not authorize api, api info is invalid !")
        return None
    #out
    return api


def get_random_api():
    #get api list
    api_list = get_api_list()
    if not api_list:
        #empty list
        return
    #choose one as random
    api_info = choice(api_list)
    #create auth object
    api = create_api(api_info)
    while(api_list and (not api)):
        api = create_api(api_list.pop())
    #
    return api

def get_users_id(api : tweepy.API):
    _target_list = []
    #get user id for each username
    for username in target_list:
        user_id = api.get_user(screen_name=username).id_str
        _target_list.append(user_id)

    return _target_list

def main():
    print(get_reply_content())
    print(get_api_list())
    
    #get an auth
    api = get_random_api()
    #empty
    if not api:
        logger.critical("The api list doesn't have any authorized api, app stopped !")
        return
    #get users numeric id and pass to target_list
    target_list = get_users_id(api)
    print(target_list)
    #get all  of api info
    api_list = get_api_list()

    #get reply content
    reply_content = get_reply_content()

    #check variables
    if not api_list:
        logger.critical("The api list is empty, app stopped !")
        return
    if not reply_content:
        logger.critical("The reply content file is empty, app stopped !")
        return

    #start streaming process
    print(figlet_format("Bot Started !"))

    for api_info in api_list:
        api_info['target_list'] = target_list
        api_info['reply_content'] = reply_content
        #start listener
        try:
            support_stream = StreamNewTweets(**api_info)
            support_stream.filter(follow=target_list, threaded=True)
        except Exception as e:
            logger.error(f"Error ro start stream")
#---------------footer--------------
if __name__ == "__main__":

    main()
#Programmer : t.me/Amir_720

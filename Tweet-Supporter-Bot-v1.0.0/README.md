# Tweet Supporter Bot

this app listen to the target list (in config.py) with many twitter accounts (api list file), when new tweet received the accounts will add it to favorite, retweet and send a reply (reply content file) for it. this is support.



### Configuration :

Set these items in **`config.py`** file :

-  `target_list` : list of accounts you want to listen to them
-  `api_list_filename` : filename that api list is in the it.
- `text_filename` : filename that reply content is in the it.



### Fill out data :

- fill out the api that you get from twitter in the file (`api_list_filename`) with this format :
  - `Consumer API Key`:`Consumer API Secret`:`Access Token`:`Access Token Secret`

- fill out the reply content to the file (`text_filename`)



### Install requirements :

```bash
pip install -r requirements.txt
```



### Start the robot : 

```bash
python3 main.py
```



#### Notice :

if the app closed, check `app.log` file.





**Author :** [t.me/Amir_720](https://t.me/Amir_720)


#Programmer : t.me/Amir_720

import json
config = {}
with open("config.json", 'r') as f:
    config = json.loads(f.read())

print('当前配置内容为：',config)

name_bot = config['name_bot']
session_name = config['session_name']
api_hash = config['api_hash']
api_id = config['api_id']
#edit this
admin = config['admin']
token = config['token']
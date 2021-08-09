# Programmer : t.me/Amir_720
####
import json
config = {}
with open("config.json", 'r') as f:
    config = json.loads(f.read())

print('当前配置内容为：',config)
print('如果修改了配置内容请手动删除 bot.session 后，重新启动')

bot_name = config['bot_name']
session_name = config['session_name']
api_hash = config['api_hash']
api_id = config['api_id']
####
token = config['token']
target_channel = config['target_channel']
admins = config['admins']

# Programmer : t.me/Amir_720
####
import json
f = open('config.json')
content = f.read()
configJson = json.loads(content)
f.close()

print(configJson)
print(configJson['api_hash'])

bot_name = configJson["bot_name"]
session_name = configJson["session_name"]
api_hash = configJson["api_hash"]
api_id = configJson["api_id"]
####

token = configJson["token"]  #token of robot from botfother
admin = configJson["admin"]     # the numeric ID of admin (management) of bot

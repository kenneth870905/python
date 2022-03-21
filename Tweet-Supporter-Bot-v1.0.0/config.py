import json
text_filename = "text.txt"
api_list_filename = "api_list.txt"
f = open('target_list.json','r')
content = f.read()
f.close()
target_list = json.loads(content)



#encoding:utf-8
f = open("1.txt")
str = ''
line = f.readline()
while line:
    str+=line
    line = f.readline()
f.close()
# str = str.replace("'",'"').replace("\n",'').replace("，",',')
list1 = str.split(',')
print(len(str))
list1 = list(set(list1))
print(len(list1))
str2 = ','.join(list1)
print(str2)

fo = open("去除重复后.txt", "r+")
fo.write( str2 )
fo.close()
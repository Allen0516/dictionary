import pymysql
#coding=utf-8

#MySQL的连接
conn = pymysql.connect(
                host='localhost',\
                port=3306,\
                user='root',\
                passwd='123456',\
                database='dict',\
                charset='utf8')
cur = conn.cursor()
f = open("/home/tarena/桌面/regex/dict.txt", "r")
while True:
    line = f.readline()
    if line:
        k=line.split(" ")
        s=len(k[0])
        l=line[s:].strip()
        g=k[0]
        print(line)
        s="insert into Dict(word,translation) values(%s,%s);"
        b=[g,l]
        cur.execute(s,b)
        conn.commit() 
    else:
        break
f.close()
cur.close()

conn.close()
 
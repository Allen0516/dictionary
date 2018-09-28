import re 
import pymysql

f= open("/home/tarena/桌面/regex/dict.txt",'r')
db = pymysql.connect(host='localhost',\
                port=3306,\
                user='root',\
                passwd='123456',\
                database='dict',\
                charset='utf8')
                
cursor = db.cursor()
for line in f:
    l  = re.split(r'\s+',line)
    
    bb = l[0]
    gg = ' '.join(l[1:])
    oo = (bb,gg)
    sql = "insert into Dict(word,translation) values(%s,%s);"
   
    try:    
        cursor.execute(sql,oo)
        db.commit()
    except:
        pass
f.close()

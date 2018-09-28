'''
name：allen
date:2018 9-28
'''
import pymysql
from socket import *
import os
import sys
import time
import signal
#定义全局变量
DICT_TEXT = "/home/tarena/桌面/regex/dict.txt"
HOST = '0.0.0.0'
PORT = 8000
ADDR=(HOST,PORT)


def main():
    #创建数据库链接
    db=pymysql.connect("localhost",'root',"123456","dict")
    #创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    #忽略字进程信号
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    while True:
        try:
           c,addr = s.accept()
           print("connect from",addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        #创建字进程
        pid = os.fork()
        if pid==0:
            s.close()
            do_child(c,db)
        else:
            c.close() 
            continue
def do_child(c,db):
    while True:#循环接受客户端请求
        data = c.recv(128).decode()
        print(c.getpeername(),":",data)

        if data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == "Q":
            do_quert(c,db,data)
        elif data[0] == "L":
            do_login(c,db,data)
        elif (not data) or data[0] =="E":
            c.close()
            sys.exit(0) 
        elif data[0] == 'H':
            do_hist(c,db,data)          
def do_login(c,db,data):
    print("登录操作")
    l = data.split(" ")
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()
    sql = "select *from user where name ='%s' and password='%s'"%(name,passwd)
    cursor.execute(sql)
    r = cursor.fetchone()
    if r== None:
        c.send(b'FALl')
    else:
        print("%s登录成功"%name)
        c.send(b'ok')

    
def do_register(c,db,data):
    print("注册操作")
    l = data.split(' ')
    name = l[1]
    passwd = l[2]
    cursor = db.cursor()
    sql = 'select *from user where name = "%s"'%name
    cursor.execute(sql)
    r= cursor.fetchone()
    if r!= None:
        c.send(b'EXISTS')
        return
    #用户不存在插入用户
    sql = "insert into user (name,password) values('%s','%s')"%(name,passwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b"ok")
    except:
        db.rollback()
        c.send(b"FALL")
    else:
        print("%s注册陈宫"%name)
def do_quert(c,db,data):
    print("查询操作")
    l = data.split(" ")
    name = l[1]
    word = l[2]
    cursor = db.cursor()

    def insert_history():
        tm = time.ctime()
        sql = "insert into hist (name,word,time) values('%s','%s','%s')"%(name,word,tm)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    #文本查询
    try:
        f= open(DICT_TEXT)
    except:
        c.send(b"FAll")
        return
    for line in f:
        tmp=line.split(" ")[0]
        if tmp > word:
            c.send(b"FALL")
            return
        elif tmp == word:
            c.send(b"ok")
            time.sleep(0.1)
            c.send(line.encode())
            f.close()
            insert_history()
            break
    c.send(b"FALl")
    f.close()
def do_hist(c,db,data):
    print("历史记录")
    l = data.split(' ')
    name = l[1]
    cursor =db.cursor()
    sql = "select *from hist where name ='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchall()
    if not r:
        c.send(b"Fall")
        return
    else:
        c.send(b"ok")
    for i in r :
        time.sleep(0.1)
        msg = "%s   %s   %s"%(i[1],i[2],i[3])
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b"##")


    

if __name__ == "__main__":
    main()
"""
author: Jocelyn
email:baccy126@126.com
time:2020-6-22
env:Python3.6
在线电子词典

c 逻辑控制， 基础结构搭建，接收请求，调用数据,数据整合提供给客户端
"""
import sys
from multiprocessing import Process
from signal import *
from socket import *
from time import sleep

from my_dict_db import DataBase

HOST = "0.0.0.0"
PORT = 6008
ADDR = (HOST, PORT)
class MyProcess(Process):
    def __init__(self, connfd):
        super().__init__()
        self.connfd=connfd
        self.db=DataBase()

    def run(self):
        while True:
            data=self.connfd.recv(1024).decode()
            temp=data.split(" ")
            if not temp or temp[0]=="E":
                break
            elif temp[0]=="R":
                print("接收到注册请求")
                self.do_register(self.connfd,temp[1],temp[2])
            elif temp[0]=="L":
                print("接收到登录请求")
                self.do_login(self.connfd,temp[1],temp[2])
            elif temp[0]=="Q":
                print("接收到查询请求")
                self.do_query(self.connfd,temp[1],temp[2])
            elif temp[0]=="H":
                print("接收到查询历史记录请求")
                self.do_history(self.connfd,temp[1])

        self.connfd.close()
        self.db.cur.close()

    def do_register(self, connfd, uname, upsw):
        print("进入注册程序")
        result=self.db.do_register(uname,upsw) #得到真或假
        if result:
            connfd.send(b"Yes")
        else:
            connfd.send(b"No")

    def do_login(self, connfd, uname, upsw):
        print("进入登录程序")
        result_uname = self.db.do_matchname(uname)
        result_upsw=self.db.do_matchpsw(upsw)
        if result_uname and result_upsw:
            connfd.send(b"Yes")
        elif not result_uname:
            connfd.send(b"WrongName")
        elif not result_upsw:
            connfd.send(b"WrongPsw")

    def do_query(self, connfd, name, word):
        self.db.insert_history(name,word)
        meaning=self.db.do_query(word)
        if meaning:
            data="%s: %s"%(word,meaning)
        else:
            data = "%s: Not Found" % word
        connfd.send(data.encode())

    def do_history(self, connfd, name):
        history=self.db.do_history(name)
        if history:
            for item in history:
                msg="%-10s %-10s %-s"%item
                connfd.send(msg.encode())
                sleep(0.1)
        else:
            connfd.send(b"No History")
        connfd.send(b"##")

def main():
    #fd是文件描述符
    sockfd=socket()
    sockfd.bind(ADDR)
    sockfd.listen(6)
    print("Listen the port %d..." % PORT)
    signal(SIGCHLD, SIG_IGN)
    while True:
        try:
            connfd, addr =sockfd.accept()
            print("Connect from", addr)
        except:
            sockfd.close()
            sys.exit("服务端退出！！")
        p=MyProcess(connfd) #这步我之前一直放在外面， 所以这句话一直飘红
        p.daemon=True
        p.start()


if __name__ == '__main__':
    main()
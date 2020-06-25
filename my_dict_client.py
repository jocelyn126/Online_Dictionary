"""
v 客户端，发送请求，接收结果展示
"""
import sys
from socket import *

HOST = "127.0.0.1"
PORT = 6008
ADDR = (HOST, PORT)

def search_word(username,c_sock):
    while True:
        print("退出查询请输入：##")
        word=input("请输入单词：")
        if word=="##":
            return
        msg="Q %s %s"%(username,word)
        c_sock.send(msg.encode())

        meaning=c_sock.recv(1024).decode()
        print(meaning)


def serch_history(username, c_sock):
    msg="H %s"%username
    c_sock.send(msg.encode())

    while True:
        history = c_sock.recv(1024).decode()
        if history=="##":
            break
        print(history)


def query_menu(username,c_sock):
    while True:
        print("=========== 查询界面 =============")
        print("***        1. 查单词           ***")
        print("***        2. 历史记录         ***")
        print("***        3. 注销             ***")
        print("=================================")

        cmd = input("请输入命令:")
        if cmd == "3":
            return  # 退出二级界面
        elif cmd =="1":
            search_word(username,c_sock)
        elif cmd=="2":
            serch_history(username,c_sock)


def register(c_sock):
    while True:
        input_username=input("请输入用户名：")
        input_psw=input("请输入密码：")
        if " " in input_username or " " in input_psw:
            print("用户名密码不能包含空格")
            continue
        msg="R %s %s"%(input_username,input_psw)
        c_sock.send(msg.encode())

        data=c_sock.recv(128).decode() #这步我一开始写的时候没解码， 导致一直跳到用户名已存在的支线去
        if data=="Yes":
            print("注册成功！")
        else:
            print("用户名已存在，是否重新输入？ Y/N")
            if input(">>")=="Y":
                continue
            else:
                return input_username
        return input_username


def do_login(c_sock):
    while True:
        input_username = input("请输入用户名：")
        input_psw = input("请输入密码：")
        if " " in input_username or " " in input_psw:
            print("用户名密码不能包含空格")
            continue
        msg="L %s %s"%(input_username,input_psw)
        c_sock.send(msg.encode())

        data = c_sock.recv(128).decode()
        if data=="Yes":
            print("登录成功！")
        else:
            if data=="WrongName":
                print("用户名错误，登录失败")
            elif data=="WrongPsw":
                print("密码错误，登录失败")
        return input_username

def main():
    c_sock=socket()
    c_sock.connect(ADDR)

    while True:
        print("=========== 登录界面 =============")
        print("***         1.登录           ***")
        print("***         2.注册         ***")
        print("***         3.退出          ***")
        print("=================================")

        cmd = input("请输入命令:")
        if cmd=="":
            c_sock.send(b"E ")
            break
        elif cmd == "1":
            user_name=do_login(c_sock)
            print("正在为您登录查询界面...")
            query_menu(user_name,c_sock)
        elif cmd == "2":
            user_name=register(c_sock)
            # print("正在为您登录查询界面...")
            # query_menu(c_sock,user_name)
        elif cmd=="3":
            c_sock.send(b"E")
            break
    sys.exit("谢谢使用")

if __name__ == '__main__':
    main()
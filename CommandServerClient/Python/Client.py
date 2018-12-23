
# Python program to implement client side of chatroom
import socket
import select
import sys

HOST = "127.0.0.1"
PORT = 20000
ADDR = (HOST, PORT)
BUFF = 2048
CLNT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLNT.connect(ADDR)

SOCK_LST = [sys.stdin, CLNT]
read_sockets, write_sockets, error_sockets = select.select(SOCK_LST, [], [])

ACTIVE = True


def parse_command(command):
    global ACTIVE
    if "say hello" in command:
        return "I was ordered to say hello"
    elif "say goodbye" in command:
        ACTIVE = False
        return "I was ordered to say goodbye"

def main():
    global ACTIVE
    while ACTIVE:
        for sock in read_sockets:
            if sock == CLNT:
                msg = sock.recv(BUFF).decode('utf-8')
                print(msg)
                resp = parse_command(msg)
                if resp is not None:
                    CLNT.send(resp.encode('utf-8'))
            else:
                pass
    CLNT.close()

if __name__ == '__main__':
    main()


# Python program to implement client side of chatroom
import socket
import select
import sys

HOST = "127.0.0.1"
PORT = 20000
ADDR = (HOST, PORT)
BUFF = 2048
CMND = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CMND.connect(ADDR)

ACTIVE = True

def main():
    global ACTIVE
    while ACTIVE:
        SOCK_LST = [sys.stdin, CMND]
        read_sockets, write_sockets, error_sockets = select.select(SOCK_LST, [], [])
        for sock in read_sockets:
            if sock == CMND:
                msg = sock.recv(BUFF).decode('utf-8')
                print(msg)
            else:
                msg = sys.stdin.readline()
                if 'quit' in msg:
                    CMND.send("Commander quitting".encode('utf-8'))
                    ACTIVE = False
                else:
                    CMND.send(msg.encode('utf-8'))
                    sys.stdout.flush()
    CMND.close()

if __name__ == '__main__':
    main()

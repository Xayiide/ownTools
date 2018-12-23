import socket
import select
import sys
import threading

HOST = "127.0.0.1"
PORT = 20000
ADDR = (HOST, PORT)
BUFF = 1024
AMNT = 5

SERV = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERV.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERV.bind(ADDR)

clients = []

def handle_client(conn, addr):
    conn.send("## Welcome ##".encode('utf-8'))
    user = str(addr[0]) + ":" + str(addr[1])
    broadcast("[!!] " + user + " connected", conn)
    while True:
        try:
            message = conn.recv(BUFF).decode('utf-8')
            if message:
                msg = "<" + user + "> " + message
                print("[+] " + msg)
                broadcast(msg, conn)
            else:
                remove(conn)
                print("[!] " + user + " disconnected")
                broadcast("[!!] " + user + " disconnected", conn)
                break
        except:
            pass

def broadcast(msg, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(msg.encode('utf-8'))
            except:
                client.close()
                remove(client)

def remove(conn):
    if conn in clients:
        clients.remove(conn)

def main():
    print("[+] Listening for connections")
    SERV.listen(AMNT)
    while True:
        conn, addr = SERV.accept()
        clients.append(conn)

        print("[+] Connection from " + str(addr[0]) + ":" + str(addr[1]))
        threading.Thread(target=handle_client, args=(conn, addr)).start()

    conn.close()
    SERV.close()

if __name__ == '__main__':
    main()

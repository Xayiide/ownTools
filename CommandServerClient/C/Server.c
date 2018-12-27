#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h> // for open
#include <unistd.h> // for close
#include <pthread.h>

#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#include <string.h>

#define HOST "127.0.0.1"
#define PORT 20000
#define BUFF 256
#define AMNT 5

char banner[BUFF] = "You reached the server\n";
int socket_array[AMNT] = {-1, -1, -1, -1, -1};
int socket_count = 0;

void broadcast(int socket, char* msg, int flags) {
    for (int conn = 0; conn < socket_count; conn++)
        if (conn != socket)
            send(socket, msg, sizeof(msg), flags);
}

void remove_socket(int client_socket) {
    int found = 0;
    if (socket_array[socket_count-1] == client_socket) {
        socket_array[socket_count-1] = -1;
    }
    for (int sock = 0; sock < socket_count -1; sock++) {
        if (socket_array[sock] == client_socket)
            found = 1;
        if (found) {
            socket_array[sock] = socket_array[sock+1];
        }
    }
    if (found)
        socket_count--;
}

void* handle_client(int client_socket, struct sockaddr_in client_addr) {
    int  connected = 1;
    char user[21]; // xxx.xxx.xxx.xxx:ppppp in the longest case
    char bcastmsg[40];
    char msg[BUFF];

    sprintf(user, "%s:%d", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
    sprintf(bcastmsg, "[!!] %s connected", user);

    send(client_socket, banner, sizeof(banner), 0);
    broadcast(client_socket, bcastmsg, 0);

    while(connected) {
        recv(client_socket, &msg, sizeof(msg), 0);
        if(strcmp(msg, "") != 0) { // If something was sent
            sprintf(msg, "<%s> %s", user, msg);
            printf("[+] %s\n", msg);
            broadcast(client_socket, msg, 0);
        }
        else { // No message received
            remove_socket(client_socket);
            sprintf(msg, "[!!] %s disconnected", user);
            printf("[+] %s disconnected\n", user);
            broadcast(client_socket, msg, 0);
            connected = 0;
        }
    }
}

int main() {
    int  serv_sock    = socket(AF_INET, SOCK_STREAM, 0); /* Create socket */
    int  clnt_sock;
    socklen_t sock_size = sizeof(struct sockaddr_in);

    /* Define addresses */
    struct sockaddr_in serv_addr;
    struct sockaddr_in clnt_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family      = AF_INET;
    serv_addr.sin_port        = htons(PORT);
    serv_addr.sin_addr.s_addr = inet_addr(HOST); /* 16777343 */

    /* Bind the socket to the address */
    bind(serv_sock, (struct sockaddr *) &serv_addr, sizeof(struct sockaddr)); /* Assign a name to the socket */
    printf("[+] Listening on [%s:%d]\n", HOST, PORT);
    listen(serv_sock, AMNT);

    while(1) {
        clnt_sock = accept(serv_sock, (struct sockaddr *) &clnt_addr, &sock_size);
        printf("[+] Connection from [%s:%d]\n", inet_ntoa(clnt_addr.sin_addr), ntohs(clnt_addr.sin_port));
        socket_array[socket_count] = clnt_sock;
        socket_count++;
        
        // New thread calling handle_client(clnt_sock, (struct sockaddr *) &clnt_addr)
        // send(clnt_sock, banner, sizeof(banner), 0);
    }
    close(serv_sock);

    return 0;
}




/*
struct sockaddr_in -> El struct para definir direcciones de red.
struct sockaddr_in {
    short            sin_family;   // e.g. AF_INET
    unsigned short   sin_port;     // e.g. htons(3490)
    struct in_addr   sin_addr;     // see struct in_addr, below
    char             sin_zero[8];  // zero this if you want to
};

struct in_addr {
    unsigned long s_addr;  // load with inet_aton()
};

struct sockaddr -> Su unico proposito es ser usado para castear el struct de
direcciones y que el compilador no tire warnings
struct sockaddr {
    sa_family_t sa_family;
    char        sa_data[14];
}








*/

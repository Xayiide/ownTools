#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h> // for open
#include <unistd.h> // for close

#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#include <string.h>

#define BUFF 256

int ACTIVE = 1;


void parse_command(char* res, char* cmd) {
    if (strcmp(cmd, "say goodbye") == 0) {
        res = "Told to say goodbye";
        ACTIVE = 0;
    }
    else {
        res = "0";
    }
}

int main() {
    char msg_rcv[BUFF];
    char msg_snd[BUFF];
    /* Create a socket */
    int network_socket = socket(AF_INET, SOCK_STREAM, 0); /* IP-TCP Socket */
    /* Specify address for the socket */
    struct sockaddr_in server_address;
    server_address.sin_family      = AF_INET; /* Protocol the server is using (IP) */
    server_address.sin_port        = htons(20000); /* Port the server is listening on */
    server_address.sin_addr.s_addr = inet_addr("127.0.0.1"); /* IP the server is listening on */

    int status = connect(network_socket, (struct sockaddr *) & server_address, sizeof(server_address));
    if (status < 0) {
        perror("ERROR connecting to the socket\n");
        exit(1);
    }

    while (ACTIVE) {
        recv(network_socket, &msg_rcv, sizeof(msg_rcv), 0);
        printf("[+] Received: %s\n", msg_rcv);
        parse_command(msg_snd, msg_rcv);
        if (strcmp(msg_snd, "0") != 0)
            send(network_socket, msg_snd, sizeof(msg_snd), 0);
    }
    close(network_socket);


    return 0;
}

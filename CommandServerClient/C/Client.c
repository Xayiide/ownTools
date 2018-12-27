#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h> // for open
#include <unistd.h> // for close

#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#include <string.h>


int main() {
    /* Create a socket */
    int network_socket = socket(AF_INET, SOCK_STREAM, 0);
    /* Specify address for the socket */
    struct sockaddr_in server_address;
    server_address.sin_family      = AF_INET;
    server_address.sin_port        = htons(20000);
    server_address.sin_addr.s_addr = inet_addr("127.0.0.1");

    int status = connect(network_socket, (struct sockaddr *) & server_address, sizeof(server_address));
    if (status < 0) {
        perror("ERROR connecting to the socket\n");
        exit(1);
    }

    char buffer[256];
    recv(network_socket, &buffer, sizeof(buffer), 0);

    printf("[+] Received: %s\n", buffer);

    close(network_socket);


    return 0;
}

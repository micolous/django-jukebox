from socket import AF_INET, SOCK_DGRAM, socket
addr = ("172.23.8.49", 8000)
s = socket(AF_INET,SOCK_DGRAM)

data = 'shutdown'
num_sent = 0
while num_sent < len(data):
    num_sent += s.sendto(data, addr)
s.close()
import socket

try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 8967

        s.connect(('127.0.0.1', port))

        print(s.recv(0xFF))

        s.close()
except:
        print("Client dun goofed.")

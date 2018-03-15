import os
import time
import socket
import multiprocessing 

port = 8967

def server():
        try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                s.bind(('', port))

                s.listen(5)
                print("Listening on port " + str(port) + ".")

                c, addr = s.accept()

                print("Connected from " + str(addr) + ".")
                while True:
                        c.send(bytes('Hey whats up? ', 'utf-8'))
                        time.sleep(0.5)

                c.close()
        except:
                print("Server dun goofed.")

def client():
        try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                s.connect(('127.0.0.1', port))

                while True: 
                        print("Client received: " + str(s.recv(0xFF)))
                        time.sleep(0.5)


                s.close()
        except:
                print("Client dun goofed.")

def main():
        p1 = multiprocessing.Process(target=server)
        p2 = multiprocessing.Process(target=client)
        p1.start()
        time.sleep(1)
        p2.start()
        
        p1.join()
        p2.join()


if __name__ == "__main__":
        main()

import os
import time
import multiprocessing 

port = 8967

def server(pwrite):
        try:
                while True:
                        os.write(pwrite, bytes('Hey whats up? ', 'utf-8'))
                        time.sleep(0.5)

                c.close()
        except:
                print("Server dun goofed.")

def client(pread):
        try:
                while True: 
                        print("Client received: " + str(os.read(pread, 0xFF)))
                        time.sleep(0.5)


                s.close()
        except:
                print("Client dun goofed.")

def main():
        pread, pwrite = os.pipe()
        p1 = multiprocessing.Process(target=server, args=(pwrite,))
        p2 = multiprocessing.Process(target=client, args=(pread, ))
        p1.start()
        #time.sleep(1)
        p2.start()
        
        p1.join()
        p2.join()
        os.close(pread)
        os.close(pwrite)


if __name__ == "__main__":
        main()

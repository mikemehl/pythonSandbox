import socket


try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 8967

        s.bind(('', port))

        s.listen(5)
        print("Listening on port " + str(port) + ".")

        c, addr = s.accept()

        print("Connected from " + str(addr) + ".")

        c.send(bytes('Hey whats up?', 'utf-8'))

        c.close()
except:
        print("Server dun goofed.")

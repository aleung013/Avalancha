import socket, select

def broadcast_data(sock,message):
    for socket in CONNECTION_LIST:
        if socket != s and socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__":
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    host = "localhost"
    port = 5000
    s.bind((host,port))
    s.listen(10)

    CONNECTION_LIST.append(s)
    print "Chat server started on port",port
    
    while True:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
        for sock in read_sockets:
            if sock == s:
                c, addr = s.accept()
                CONNECTION_LIST.append(c)
                print 'Got connection from', addr
                broadcast_data(c,"\n[%s:%s] has connected\n" % addr)
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data != "quit":
                        broadcast_data(sock, "\r"+"<"+str(sock.getpeername())+"> "+data)
                    elif data == "quit":
                        print addr, "has gone offline"
                        broadcast_data(sock,"\nClient (%s, %s) is offline\n" % addr)
                        CONNECTION_LIST.remove(sock)
                        #c.close()
                except:
                    print "Lost connection from", addr
                    broadcast_data(sock,"Client (%s, %s) is offline\n" % addr)
                    CONNECTION_LIST.remove(sock)
                    c.close()
    s.close()

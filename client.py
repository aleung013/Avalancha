import socket, select, string, sys,pickle

def prompt():
    sys.stdout.write('<You> ')
    sys.stdout.flush()

if __name__ == "__main__":
    #if len(sys.argv) < 3:
    #    print 'Usage : python telnet.py hostname port'
    #    sys.exit()

    host = "localhost"
    port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((host,port))
    except:
        print 'Unable to connect.'
        sys.exit()

    print 'Connected to server.'

    while True:
        try:
            socket_list = [sys.stdin, s]
            read_sockets,write_sockets,error_sockets = select.select(socket_list,[],[])
            for sock in read_sockets:
                if sock == s:
                    data = sock.recv(4096)
                    if not data:
                        print '\nDisconnected from server.'
                        sys.exit()
                    elif (data == "game_size"):
                        sys.stdout.write("How big should the game be?\n")
                        prompt()
                        msg = sys.stdin.readline()
                        s.send(msg)
                    elif (data == "bull_"):
                        sys.stdout.write("BULLSHIT")
                    elif (data == "send_cards"):
                        print "waiting for cards"
                        sock.send("ready for cards")
                        data = sock.recv(4096)
                        sys.stdout.write("Cards received: \n")
                        serStr = pickle.loads(data)
                        print serStr
                        #sys.stdout.write(repr(serStr))
                    else:
                        sys.stdout.write(data)
                else:
                    msg = sys.stdin.readline()
                    s.send(msg)
                    prompt()
        except:
            s.send("quit")
            s.close()
            sys.exit()

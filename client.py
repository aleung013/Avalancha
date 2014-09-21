import socket, select, string, sys
from communistpoker import COMBOS
from deck import VALUES,SUITS
def parseCombo(msg):
    combo = []
    for i in range(len(COMBOS)):
        if(msg.find(COMBOS[i])):
            combo[0] = COMBOS[i]
    if(combo[1] == COMBOS[3]):#Flush
        for i in range(len(SUITS)):
            if(msg.find(SUITS[i])):
                combo[1] = COMBOS[i]
    

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
                        data = sock.recv(4096)
                        sys.stdout.write("Cards received: \n")
                        sys.stdout.write(data)
                    elif (data == "play_round"):
                        data = sock.recv(4096) #get the old combo
                        sys.stdout.write("What do you call?\n")
                        msg = sys.stdin.readline()
                        combo = parseCombo(msg)
                        s.send(combo)
                        
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

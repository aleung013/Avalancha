import socket, select,communistpoker

def broadcast_data(sock,message):
    for socket in CONNECTION_LIST:
        if socket != s:
            if sock== None or socket != sock:
                try:
                    socket.send(message)
                except:
                    socket.close()
                    CONNECTION_LIST.remove(socket)
                    print 'A player got disconnected\n'

if __name__ == "__main__":
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    host = "localhost"
    port = 5000
    s.bind((host,port))
    s.listen(10)      #maybe set to lower number or somehow make "games" instead of just server

    CONNECTION_LIST.append(s)
    print "Chat server started on port",port
    
    game_size = 10;
    player_names = []
    playerNumCard=[]
    while True:
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
        if(len(CONNECTION_LIST)-1< game_size):  #if game is not full
            for sock in read_sockets:
                if sock == s:
                    c, addr = s.accept()
                    player_names.append(addr)
                    CONNECTION_LIST.append(c)
                    print 'Got connection from', addr
                    broadcast_data(c,"\n[%s:%s] has connected\n" % addr)
                    if len(CONNECTION_LIST)==2:
                        c.send("game_size") #asks the first player how many player game it will be
                        try: 
                            game_size = int(c.recv(RECV_BUFFER))
                        except:
                            print addr," returned invalid value.\n"
                else:
                    try:
                        data = sock.recv(RECV_BUFFER)
                        if data != "quit":
                            broadcast_data(sock, "\r"+"<"+str(sock.getpeername())+"> "+data)
                        elif data == "quit":
                            print addr, "has gone offline"
                            broadcast_data(sock,"\nClient (%s, %s) is offline\n" % addr)
                            player_names.remove(player_names[CONNECTION_LIST.index(sock)])
                            CONNECTION_LIST.remove(sock)
                            #c.close() cause closed by the other side? supposedly
                    except:
                        print "Lost connection from", addr
                        broadcast_data(sock,"Client (%s, %s) is offline\n" % addr)
                        player_names.remove(player_names[CONNECTION_LIST.index(sock)])
                        CONNECTION_LIST.remove(sock)                        
                        c.close()

        else: #game is full -> game start now
            if len(playerNumCard)==0:
                playerNumCard = [1 for i in range(len(playerlist))]
            data=roundData(player_names,1,5,playerNumCard)
            for i in range(len(player_names)):
                try:
                    CONNECTIONS_LIST[i].send(data[1][i])
                except:
                    print "couldn't send hand to player\n"
                    break
            player_turn = 0;
            while True:
                cur_player = (player_turn%game_size)+1
                try:
                    CONNECTIONS_LIST[cur_player].send("play_round")
                except:
                    print "\nlost connection from player ",cur_player-1
                    player_names.remove(player_names[cur_player])
                    CONNECTION_LIST.remove(read_sockets[cur_player])
                    break
                try:
                    response = CONNECTIONS_LIST[cur_player].recv(RECV_BUFFER)
                    if response == "bull_":
                        try:
                            CONNECTIONS_LIST[cur_player].send("send_hand")
                            hand = CONNECTIONS_LIST[cur_player].recv(RECV_BUFFER)
                            combo = CONNECTIONS[cur_player].recv(RECV_BUFFER)
                            if not bull(hand,combo):
                                 endRound(player_names,1,5,playerNumCard,cur_player-1)
                            else:
                                endRound(player_names,1,5,playerNumCard,cur_player-2)
                        except:
                            print "\nlost connection to player",cur_player
                            player_names.remove(player_names[cur_player])
                            CONNECTION_LIST.remove(read_sockets[cur_player])
                            break                      
                    else:
                        broadcast_data(read_sockets[cur_player],response)
                        player_turn += 1
                except:
                    print "\nlost connection from player or lack of response ",cur_player-1
                    player_names.remove(player_names[cur_player])
                    CONNECTION_LIST.remove(read_sockets[cur_player])
                    break
                    
    s.close()

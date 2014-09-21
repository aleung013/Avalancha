import socket, select,sys,pickle
from communistpoker import roundData, endRound, bull

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
    print "Game server started on port",port
    
    game_size = 10;
    playerNumCard=[]
    while True:
        if(len(CONNECTION_LIST)-1 < game_size):  #if game is not full
            read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
            for sock in read_sockets:
                if sock == s:
                    c, addr = s.accept()
                    CONNECTION_LIST.append(c)
                    print 'Got connection from', addr
                    broadcast_data(c,"\n[%s:%s] has connected" % addr)
                    if len(CONNECTION_LIST)==2:
                        c.send("game_size") #asks the first player how many player game it will be
                        try: 
                            game_size = int(c.recv(RECV_BUFFER))
                            print game_size," players\n"
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
                            CONNECTION_LIST.remove(sock)
                            #c.close() cause closed by the other side? supposedly
                    except:
                        print "Lost connection from", addr
                        broadcast_data(sock,"Client (%s, %s) is offline\n" % addr)
                        CONNECTION_LIST.remove(sock)                        
                        c.close()

        else: #game is full -> game start now
            print "Beginning game"
            if len(playerNumCard)==0:
                playerNumCard = [1 for i in range(len(CONNECTION_LIST)-1)]
            data=roundData(CONNECTION_LIST[1:],1,5,playerNumCard)
            for i in range(len(CONNECTION_LIST)-1):
                CONNECTION_LIST[i+1].send("send_cards")
                try:
                    CONNECTION_LIST[i+1].recv(RECV_BUFFER)
                    serStr = pickle.dumps(data[1][i])
                    CONNECTION_LIST[i+1].send(serStr)
                except:
                    print "couldn't send hand to player\n"
                    exit(1)
            player_turn = 0;
            while True:
                cur_player = (player_turn%game_size)
                try:
                    CONNECTION_LIST[cur_player+1].send("play_round")
                except:
                    print "\nlost connection from player ",cur_player
                    CONNECTION_LIST.remove(read_sockets[cur_player])
                    break
                try:
                    response = CONNECTION_LIST[cur_player+1].recv(RECV_BUFFER)
                    if response == "bull_":
                        try:
                            CONNECTION_LIST[cur_player].send("send_hand")
                            hand = CONNECTION_LIST[cur_player].recv(RECV_BUFFER)
                            combo = CONNECTION_LIST[cur_player].recv(RECV_BUFFER)
                            if not bull(hand,combo):
                                 endRound(CONNECTION_LIST[1:],1,5,playerNumCard,cur_player-1)
                            else:
                                endRound(CONNECTION_LIST[1:],1,5,playerNumCard,cur_player-2)
                        except:
                            print "\nlost connection to player",cur_player
                            CONNECTION_LIST.remove(read_sockets[cur_player])
                            break                      
                    else:
                        broadcast_data(read_sockets[cur_player],response)
                        player_turn += 1
                except:
                    print "\nlost connection from player or lack of response ",cur_player-1
                    CONNECTION_LIST.remove(read_sockets[cur_player])
                    break
                    
    s.close()

from deck import standardDeck, shuffle, dealUneven, sort, VALUES, SUITS

COMBOS = ['SINGLE',
          'DOUBLE',
          'TRIPLE',
          'FLUSH',
          'STRAIGHT',
          'FULLHOUSE',
          'BOMB',
          'STRAIGHTFLUSH',
          'FIVEKIND',
          'SIXKIND',
          'SEVENKIND',
          'EIGHTKIND']

def startRound(numplayers,cardsperplayer):
    deck = standardDeck()
    print "Shuffling..."
    shuffle(deck)
    print "Dealing..."
    players = dealUneven(deck,numplayers,cardsperplayer)
    return players
    
def roundData(playerlist,startcards,endcards,cardsperplayer):
    players = startRound(len(playerlist),cardsperplayer)
    currplayer = 0
    for i in range(len(playerlist)):
        print playerlist[i],':',players[i]
    return (playerlist,players)

def endRound(playerlist,startcards,endcards,cardsperplayer,losingPlayer):
    cardsperplayer[losingPlayer]++
    for i in range(len(playerlist)):
        if (cardsperplayer[i] > endcards):
            cardsperplayer[i] = 0
    return
    
def countValue(cards,value,cap = 8,suit = None):#Does not count 2's
    if(suit):
        s = sum(1 for card in cards if card['value'] == value and card['suit'] == suit)
    else:
        s = sum(1 for card in cards if card['value'] == value)
    if s > cap:
        s = cap
    return s

def countSuit(cards,suit):#Does not count 2's
    return sum(1 for card in cards if card['suit'] == suit and card['value'] != '2')

def checkCards(players,combo):
    cards = []
    for p in players:
        cards.extend(p)
    c = combo[0]
    if c == COMBOS[0]:#SINGLE
        return countValue(cards,combo[2]) + countValue(cards,'2') >= 1
    elif c == COMBOS[1]:#DOUBLE
        return countValue(cards,combo[2]) + countValue(cards,'2') >= 2
    elif c == COMBOS[2]:#TRIPLE
        return countValue(cards,combo[2]) + countValue(cards,'2') >= 3
    elif c == COMBOS[3]:#FLUSH
        return countSuit(cards,combo[1]) + countValue(cards,'2') >= 5
    elif c == COMBOS[4]:#STRAIGHT
        start = VALUES.index(combo[2])
        end = VALUES.index(combo[3])
        count = 0
        for i in range(start,end+1):
            count += countValue(cards,VALUES[i],1)
        return count + countValue(cards,'2') >= 5
    elif c == COMBOS[5]:#FULLHOUSE
        return countValue(cards,combo[2],3) + countValue(cards,combo[3],2) + countValue(cards,'2') >= 5
    elif c == COMBOS[6]:#BOMB
        return countValue(cards,combo[2],4) + countValue(cards,combo[3],1) + countValue(cards,'2') >= 5
    elif c == COMBOS[7]:#STRAIGHTFLUSH
        suit = combo[1]
        start = VALUES.index(combo[2])
        end = VALUES.index(combo[3])
        for i in range(start,end+1):
                count += countValue(cards,Values[i],1,suit)
        return None
    elif c == COMBOS[8]:#FIVEKIND
        return countValue(cards,combo[2]) + countValue(cards,'2') >= 5
    elif c == COMBOS[9]:#SIXKIND
        return countValue(cards,combo[2]) + countValue(cards,'2') >= 6
    elif c == COMBOS[10]:#SEVENKIND
        return countValue(cards,combo[2]) + countValue(cards,'2') >= 7
    elif c == COMBOS[11]:#EIGHTKIND
        return countValue(cards,combo[2]) + countValue(cards,'2') >= 8


if __name__ == '__main__':
    playerlist = ['Alvin','Vivian','Lucy','Alan','Michele']
    cardsperplayer = [1 for i in range(len(playerlist))]
    run(playerlist,1,5,cardsperplayer)

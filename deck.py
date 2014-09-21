from random import randint

VALUES = '23456789TJQKA'
SUITS = ['diamonds','clubs','hearts','spades']

def shuffle(deck):
    spot = len(deck) - 1
    while(spot > 1):
        rand = randint(0,spot)
        deck[spot],deck[rand] = deck[rand],deck[spot]
        spot -= 1


def deal(deck,numplayers = 4,cardsperhand = 13):
    return dealUneven(deck,numplayers,[cardsperhand for i in range(numplayers)])

def dealUneven(deck,numplayers = 4,cardsperhand = [1,1,1,1]):
    assert(numplayers == len(cardsperhand))
    players = [[] for i in range(numplayers)]
    stop = [0 for i in range(numplayers)]
    temp = [cardsperhand[i] for i in range(numplayers)]
    player = 0
    while (deck != [] and temp != stop):
        if(temp[player] != 0):
            players[player].append(deck.pop())
            temp[player] -= 1
        player = (player + 1)%numplayers

    return players

def standardDeck():
    return [{'value':val,'suit':suit} for suit in SUITS for val in VALUES]

def sort(cards):
    cards.sort(key = lambda x: (SUITS.index(x['suit']),VALUES.index(x['value'])))
    return cards

if __name__ == '__main__':
    deck = standardDeck()
    p =  deal(deck,4,13)
    p = [sort(x) for x in p]
    for x in p:
        print x

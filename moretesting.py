from tkinter import *
from graphics import *

master = Tk()
win = Canvas(master, width =200, height=100)
win.pack()
win.create_rectangle(10,10, 190, 90)
win.create_text((95,50),text='Communist Poker', font = (20))


def closewindow():
    exit()
    
def rules():
    rule = Tk()
    rulescreen = Canvas(rule, width = 500, height = 500)
    rulescreen.pack()
    rulescreen.create_text((250,245),text='''   Each player is given two cards at the start.
                      Beginning with the dealer, each player takes turns bidding
                      what they believe to be the highest possible hand
                      that can be formed by pooling the cards of all the players
                      into one giant hand. This goes on until one player calls
                      "BS" on the person before them, and at this point
                      everyone reveals their cards. If the bid is correct, the
                      player calling "BS" gains a card the next round.
                      If the bid is not correct,the player who made the bid
                      gains the card the next round. The game continues with a
                      new round, and players drop out of the game and lose
                      once they reach six cards. The last player remaining
                      is the winner.''')

def playsolo():
    return

def playmulti():
    return
    
v = IntVar()


playgame = Radiobutton(master, text = "Play vs Ai", variable = v, value = playsolo).pack(anchor = W)
playgame = Radiobutton(master, text = "Play vs Friends", variable = v, value = playmulti).pack(anchor = W)  
howtoplay = Button(master, text = "How to Play", command=rules,padx = 20)
howtoplay.pack(side=LEFT)
closewindow = Button(master, text = "Close Window", command=closewindow, padx = 20)
closewindow.pack(side=LEFT)


howtoplay.pack()
closewindow.pack()

#mainloop()

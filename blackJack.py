# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False # in_play shows if player still plays
outcome = ""
score = 0


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
         
# define hand class
class Hand:
    def __init__(self):
        self.cards=[]

    def __str__(self):
        for i in range(len(self.cards)):
            print self.cards[i]

    def add_card(self, card):
        self.cards.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        total=0
        for i in range(len(self.cards)):
            rank_val=self.cards[i].get_rank()
            total+=VALUES[rank_val]
     
        if total<=11:
             for j in range(len(self.cards)):
                rank_val=self.cards[j].get_rank()
                if rank_val=='A':
                    total+= 10
        return total
    
    def busted(self):
        return self.get_value()>21    
    
    def draw(self, canvas, p):
        for i in range(len(self.cards)):
            self.cards[i].draw(canvas,p)
            # give 30 pixels space if there are more than 5 cards on the table, else 80 pixels
            if i>=4:
                p[0]+=30
            else:
                p[0]+=80   
        
# define deck class
class Deck:
    def __init__(self):
        self.d_cards=[]
        for s in SUITS:
            for r in RANKS:
                self.d_cards.append(Card(s,r))

    # add cards back to deck and shuffle
    def shuffle(self):
        self.__init__()
        random.shuffle(self.d_cards)

    def deal_card(self):
        return self.d_cards.pop(0) 

#define event handlers for buttons
def deal():
    global outcome, in_play, d, ph, dh,score
    # Player lose if (s)he hits the "Deal" button in the middle of the hand
    if in_play:
        score-=1
    d.shuffle()    
    
    ph.__init__()
    ph.add_card(d.deal_card())
    ph.add_card(d.deal_card())

    dh.__init__()
    dh.add_card(d.deal_card())
    dh.add_card(d.deal_card())
    
    outcome="Hit or stand?"
    in_play = True

def hit():
    global outcome, score, in_play
 
    # if the hand is in play, hit the player
    if in_play:
        i=d.deal_card()
        ph.add_card(i)
       
        # if busted, assign an message to outcome, update in_play and score
        if ph.busted():
            outcome= "You have busted. New Deal?"
            in_play = False
            score-=1
       
def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global outcome, score, in_play
    if in_play:
        
        while dh.get_value()<17:
            dh.add_card(d.deal_card())
                
        # if busted, assign an message to outcome, update in_play and score
        if dh.busted():
            outcome= "Dealer has busted. New Deal?"
            in_play = False
            score+=1
        # assign a message to outcome, update in_play and score
        elif ph.get_value()<=dh.get_value():
            outcome= "Dealer won. New Deal?"
            in_play = False
            score-=1
        else:
            outcome= "Player won. New Deal?"
            in_play = False
            score+=1
    
# draw handler    
def draw(canvas):
    canvas.draw_text("Blackjack", (100, 50), 36, "Cyan")
    canvas.draw_text("Score:" + str(score), (350, 50), 26, "Yellow")
    canvas.draw_text("Dealer", (100, 100), 26, "White")
    dh.draw(canvas, [100, 150])
    # cover the dealer 2nd card
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,  [180 + CARD_BACK_CENTER[0], 150 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
    canvas.draw_text("Player", (100, 300), 26, "White")
    ph.draw(canvas, [100, 350])
    canvas.draw_text(outcome, (100, 500), 26, "Black")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
d=Deck()
ph = Hand()
dh = Hand()
deal()

# get things rolling
frame.start()


# remember to review the gradic rubric

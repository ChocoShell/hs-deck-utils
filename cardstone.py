import requests
import io
import simplejson as json


# read API keys
with io.open('config_secret.json') as cred:
    creds = json.load(cred)

class Card():
    def __init__(self, name):
        self.name = name
        self.id, self.image = self.get_data()

    def get_data(self):
        # These code snippets use an open-source library. http://unirest.io/python
        response = requests.get("https://omgvamp-hearthstone-v1.p.mashape.com/cards/" + self.name + "?collectible=1",
            headers={
                "X-Mashape-Key": creds['api_key'],
                "Accept": "application/json"
            }
        )
        try:
            data = response.json()[0]
        except KeyError:
            print self.name
        return (data['cardId'], data['img'])

def get_deck(filename):
    """
    Parses deck list into a list of 30 card strings.
     - filename - String with file name
    """
    content = [
        (
          int(line.rstrip('\n').split(' ', 1)[0]),
          line.rstrip('\n').split(' ', 1)[1]
        ) 
        for line in open(filename)
    ]
    deck = []
    for card in content:
        for num in range(card[0]):
            deck.append(Card(card[1]))
    return deck

def start_hand(deck, onCoin):
    """
    Gets starting hand from deck.
      - deck - List of strings containing cards in deck
      - onCoin - Boolean determining whether or 
                  not we will start with 4 cards of 3.
    """
    size = 4 if onCoin else 3
    return [deck.pop() for i in range(size)]

def mulligan(deck, hand, mull):
    """
    Remove 3 cards from deck list and prints them out
      - deck - List of strings containing cards in deck
      - hand - List of cards in hand to be replaced
    """
    mulled = []
    for letter in mull:
        mulled.append(hand[ord(letter) - 49])
        try:
            hand[ord(letter) - 49] = deck.pop()
        except IndexError:
            print "{} not in index".format(ord(letter) - 49)

    deck.extend(mulled)
    return hand

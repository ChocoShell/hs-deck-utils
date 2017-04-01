# React
# Hand - Card - Image
# Add types

from random import shuffle
import cardstone
from PIL import Image
import urllib
import io


def stitch_list(image_list):
    """
    Stitch list of filenames that lead to images that are the same size.
    """
    images = len(image_list)
    base = Image.open(image_list[0])
    width,height = base.size
    mode = base.mode
    final_im = Image.new(mode, (width, height*images))
    for i in range(images):
        im = Image.open(image_list[i])
        final_im.paste(im, (0, height*i, width, height*(i+1)))
    return final_im

def showImage(URL):
    fd = urllib.urlopen(URL)
    image_file = io.BytesIO(fd.read())
    Image.open(image_file).show()

def getImage(url):
    fd = urllib.urlopen(url)
    image_file = io.BytesIO(fd.read())
    return image_file
    
def prettyPrint(word, i):
    tabs = ''.join(['\t' for s in xrange(3 - (len(word)+3)/8)])
    print " - " + word + tabs + "[" + chr(i+48) + "]"

def main(filename):
    # Different Input
    deck = cardstone.get_deck(filename)

    # Shuffle decklist
    shuffle(deck)

    # User Input
    onCoin = raw_input("Are you going first? (y or n) ")
    onCoin = onCoin[0] == 'n'

    hand = cardstone.start_hand(deck, onCoin)
    hand_images = [getImage(hand[i].image) for i in range(len(hand))]

    stitch_list(hand_images).show()

    # Different Input
    mull = raw_input("What will you mulligan? ")
    mull = ''.join(sorted(mull.strip(" ")))
    cardstone.mulligan(deck, hand, mull)

    hand_images = [getImage(hand[i].image) for i in range(len(hand))]

    stitch_list(hand_images).show()
    shuffle(deck)

    inp = raw_input("")
    turn = 1
    while(inp != "n" and deck):
        if inp == "d":
            header = "Draw"
        else:
            header = "Turn " + str(turn)
            turn += 1
        print header + " - " + deck.pop().name
        inp = raw_input("")


main("deck1.txt")

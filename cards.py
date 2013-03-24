# encoding: utf-8

import random

class DeckEmptyError(Exception):
  pass

class card:
  # rank is 1 (ace) to 13 (King)
  # suit is 0-3, hearts, clubs, diamonds, spades
  def __init__(self, rank, suit):
    self.rank = rank
    self.suit = suit

  def __repr__(self):
    RANKS=('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
    SUITS=('♡', '♣', '♢', '♠')
    return RANKS[self.rank-1]+SUITS[self.suit]

class deck:
  def __init__(self, deckCount=1):
    self.deck = []
    for deckNumber in range(0, deckCount):
      for suit in range(4):
        for rank in range(1, 14):
          self.deck.append(card(rank, suit))

    self.nextCardIndex = 0

  def shuffle(self):
    random.shuffle(self.deck)
    self.nextCardIndex = 0

  def dealone(self):
    try:
      nextCard = self.deck[self.nextCardIndex]
    except IndexError:
      raise DeckEmptyError
    self.nextCardIndex += 1
    return nextCard

  def deal(self, count=1):
    return [self.dealone() for i in range(count)]

  def getCardCount(self):
    return len(self.deck)-self.nextCardIndex

  def __repr__(self):
    return ' '.join(str(x) for x in self.deck[self.nextCardIndex:])

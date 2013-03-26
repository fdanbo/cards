
from bjhand import bjhand

class bjplayerhand:
  def __init__(self, strategy, bet):
    self.hand = bjhand()
    self.bet = bet
    self.strategy = strategy
    self.closed = False
    self.settled = False

  def dealCard(self, card):
    self.hand.addCard(card)
    if self.hand.value() >= 21:
      self.closed = True

  def cardCount(self):
    return self.hand.cardCount()

  def checkBusted(self):
    v = self.hand.value()
    if v > 21:
      self.settleFor_(-1)
    elif v == 21:
      self.closed = True

  def canMakeMove(self, move):
    if move == 'stand':
      return True
    if move == 'hit':
      return not self.closed

    # we must have exactly two cards in any other case
    if self.hand.cardCount() != 2:
      return False

    if move == 'double' or move == 'surrender':
      # any two cards is fine
      return True

    if move == 'split':
      # can only split cards with the same value
      v1 = bjhand.cardvalue(self.hand.firstCard())
      v2 = bjhand.cardvalue(self.hand.secondCard())
      return v1 == v2

  def settle(self, dealerValue):
    assert(not self.settled)
    assert(self.hand.value() <= 21)

    if dealerValue > 21:
      # dealer busted
      self.settleFor_(1)
    else:
      myValue = self.hand.value()
      if myValue < dealerValue:
        self.settleFor_(-1)
      elif myValue == dealerValue:
        self.settleFor_(0)
      else:
        self.settleFor_(1)

  def settleFor_(self, multiplier):
    self.closed = True
    self.settled = True
    self.bet *= float(multiplier)

  def settleBlackjack(self):
    assert(self.hand.cardCount()==2)
    if self.hand.value() == 21:
      self.settleFor_(1.5)

  def makeMove(self, move, deck):
    assert(not self.closed)

    if move == 'stand':
      self.closed = True
      return

    if move == 'hit':
      self.hand.addCard(deck.dealone())
      self.checkBusted()
      return

    if move == 'double':
      self.hand.addCard(deck.dealone())
      self.bet *= 2.0
      self.closed = True
      self.checkBusted()
      return

    elif move == 'surrender':
      self.settleFor_(-0.5)
      return

    elif move == 'split':
      h1 = bjplayerhand(self.strategy, self.bet)
      h1.dealCard(self.hand.firstCard())
      h2 = bjplayerhand(self.strategy, self.bet)
      h2.dealCard(self.hand.secondCard())
      return (h1, h2)

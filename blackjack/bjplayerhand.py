
from .bjhand import bjhand
from .bjsql import bjplay

class bjplayerhand:
  def __init__(self, strategy, bet):
    self.hand = bjhand()
    self.bet = bet
    self.strategy = strategy
    self.closed = False
    self.settled = False
    self.dataToSave = []

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

  def canMakeMove(self, move, splitAllowed, surrenderAllowed):
    if move == 'stand':
      return True
    if move == 'hit':
      return not self.closed

    # we must have exactly two cards in any other case
    if self.hand.cardCount() != 2:
      return False

    if move == 'double':
      # any two cards can be doubled
      return True

    if move == 'surrender':
      # surrender is disallowed only after a split
      return surrenderAllowed

    if move == 'split':
      # if we already have 4 hands, splitAllowed will be false.  otherwise, the card values must be
      # the same.
      if not splitAllowed: return False
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
    last = len(self.dataToSave)-1
    for i,dbObject in enumerate(self.dataToSave):
      dbObject.handResult = int(self.bet*10)
      dbObject.final = (i==last)
      dbObject.save()

    self.dataToSave = []

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

  def checkpointToDB(self, dealerCard, move, canSplit, canSurrender):
    # correct canSplit to also check that the cards are the same (it only checks that we have fewer
    # than four hands)
    canSplit = canSplit and self.canMakeMove('split', canSplit, canSurrender)
    canSurrender = canSurrender and self.canMakeMove('surrender', canSplit, canSurrender)
    dbObject = bjplay(handValue=self.hand.value(),
                      soft=self.hand.soft(),
                      dealerRank=bjhand.cardvalue(dealerCard),
                      canHit=not self.closed,
                      canSplit=canSplit and not self.closed,
                      canDouble=self.hand.cardCount()==2 and not self.closed,
                      canSurrender=canSurrender and not self.closed,
                      move=move)
    # add to the list of things to save after we settle
    self.dataToSave.append(dbObject)

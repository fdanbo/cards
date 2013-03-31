
import cards
from . import bjstrategies
from .bjhand import bjhand
from .bjplayerhand import bjplayerhand

import logging

BET_AMOUNT = 1.0

class playerstate:
  def __init__(self, strategy):
    self.strategy = strategy
    self.balance = 0.0

  def __repr__(self):
    return str(self.balance)

  def startNewHand(self, bet):
    self.hands_ = [bjplayerhand(self.strategy, bet)]

  # call this once for each of the first two cards
  def dealCard(self, card):
    self.hands_[0].dealCard(card)

  def play(self, dealerUpCard, deck):
    handsToPlay = self.hands_
    self.hands_ = []
    while len(handsToPlay):
      currentHand = handsToPlay.pop()

      # if this hand was a result of a split, it will only have one card, so we have to add another.
      if currentHand.cardCount() < 2:
        currentHand.dealCard(deck.dealone())
        # enforce only one card on a split Ace
        if currentHand.hand.firstCard().rank == 1:
          currentHand.closed = True
        # enfore surrender not allowed after a split
        surrenderAllowed = False
      else:
        # check for blackjack.  the fact that this is inside the "else" ensures that we don't pay
        # blackjack after a split -- ace-ten after a split is just a normal 21.
        currentHand.settleBlackjack()

        # we're setting this to true even though we may have more than 2 cards -- really this
        # boolean means "this hand was not just split".  having 2 cards is checked later, in
        # canMakeMove().
        surrenderAllowed = True

      splitResult = None
      while not currentHand.closed:
        # enforce only splitting to four hands
        handCount = len(handsToPlay) + len(self.hands_) + 1
        splitAllowed = handCount < 4
        move = self.chooseMove(currentHand, dealerUpCard,
                               splitAllowed, surrenderAllowed)
        splitResult = currentHand.makeMove(move, deck)
        if splitResult is not None:
          # we split
          handsToPlay.append(splitResult[0])
          handsToPlay.append(splitResult[1])
          break

      if splitResult is None:
        logging.debug(currentHand.hand)
        self.hands_.append(currentHand)
        if currentHand.settled:
          # 'bet' is set to negative if we lost
          self.balance += currentHand.bet

  def settle(self, dealerValue):
    for h in self.hands_:
      if not h.settled:
        h.settle(dealerValue)
        # 'bet' is set to negative if we lost
        self.balance += h.bet

  def settleDealerBJ(self):
    logging.debug(self.hands_[0].hand)

    # TODO: insurance?
    assert(len(self.hands_)==1)
    assert(self.hands_[0].cardCount() == 2)
    self.hands_[0].settle(21)
    self.balance += self.hands_[0].bet

  def chooseMove(self, currentHand, dealerUpCard,
                 splitAllowed, surrenderAllowed):
    h = currentHand.hand
    section = self.strategy[bjhand.cardvalue(dealerUpCard)]
    handKey = h.value()
    if h.soft():
      handKey = 's'+str(handKey)
    for move in section[handKey].split(','):
      if currentHand.canMakeMove(move, splitAllowed, surrenderAllowed):
        return move
    return 'stand'


class table:
  def __init__(self, deckCount=1):
    self.deck = cards.deck(deckCount)
    self.deck.shuffle()

  def __repr__(self):
    return ' '.join([str(x) for x in self.playerStates])

  def setPlayers(self, playerStrategyList):
    self.playerStates = [playerstate(x) for x in playerStrategyList]

  def playHand(self):
    # by rule, if there are less than two decks left, we reshuffle
    if self.deck.getCardCount() < 104:
      self.deck.shuffle()

    # start new hands
    for s in self.playerStates:
      s.startNewHand(BET_AMOUNT)
    self.dealerHand = bjhand()

    # deal two cards to everyone
    for i in range(2):
      for s in self.playerStates:
        s.dealCard(self.deck.dealone())
      self.dealerHand.addCard(self.deck.dealone())

    dealerHasBlackjack = (self.dealerHand.value() == 21)

    # now have everyone play their hands. this settles hands that busted, got blackjack, or lost to
    # a blackjack.
    for s in self.playerStates:
      logging.debug('================')
      if dealerHasBlackjack:
        s.settleDealerBJ()
      else:
        s.play(self.dealerHand.firstCard(), self.deck)

    # play dealer turn. TODO: hit soft 17
    while self.dealerHand.value() < 17:
      self.dealerHand.addCard(self.deck.dealone())
    logging.debug('=====DEALER=====')
    logging.debug(self.dealerHand)

    # settle remaining bets
    dealerValue = self.dealerHand.value()
    for s in self.playerStates:
      s.settle(dealerValue)


def runtest(deckCount, playerCount, handCount,
            loggingLevel=logging.WARNING):
  # just play one hand, printing details
  logging.basicConfig(level=loggingLevel)
  mytable = table(deckCount)
  mytable.setPlayers([bjstrategies.S1 for x in range(playerCount)])
  for i in range(handCount):
    mytable.playHand()
  print('balances: {}'.format(mytable))

def splittest(deckCount, playerCount, handCount,
            loggingLevel=logging.WARNING):
  # just play one hand, printing details
  logging.basicConfig(level=loggingLevel)
  mytable = table(deckCount)
  mytable.setPlayers([bjstrategies.MISTER_SPLITTER for x in range(playerCount)])
  for i in range(handCount):
    mytable.playHand()
  print('balances: {}'.format(mytable))

def test1():
  runtest(8, 8, 1, logging.DEBUG)

def test2():
  runtest(8, 8, 100000)

def stest1():
  splittest(8, 8, 1, logging.DEBUG)

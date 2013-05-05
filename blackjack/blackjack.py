
import cards
from . import bjstrategies
from .bjhand import bjhand
from .bjplayerhand import bjplayerhand
from .bjsql import bjplay

import logging

class playerstate:
  def __init__(self, strategy, bettingStrategy):
    self.strategy = strategy
    self.bettingStrategy = bettingStrategy
    self.balance = 0.0
    self.currentHandBalance = 0.0
    self.totalBets = 0.0
    self.handCount = 0
    self.bettingState = self.bettingStrategy["initial"]

  def __repr__(self):
    return '{pct:.2f}%'.format(pct=self.balance/self.totalBets*100.0)

  def startNewHand(self, isNewShoe):
    assert(self.currentHandBalance == 0)

    # restart the betting scheme if starting a new shoe
    if isNewShoe:
      self.bettingState = self.bettingStrategy["initial"]

    bet = self.bettingState["bet"]
    logging.debug("bet is {bet}".format(bet=bet))
    self.hands_ = [bjplayerhand(self.strategy, bet)]

    self.totalBets += bet
    self.handCount += 1

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

        # surrender is allowed because we just started this hand and didn't come out of a split
        surrenderAllowed = True

      splitResult = None

      if currentHand.closed:
        # no moves to make, just log the object in the database.  this happens on blackjack and
        # after splitting aces.
        # currentHand.checkpointToDB(dealerCard=dealerUpCard, move=None, canSplit=False,
        # canSurrender=False)
        pass

      else:
        # play the hand
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
        # we finished playing the hand -- print it out
        logging.debug(currentHand.hand)
        self.hands_.append(currentHand)
        if currentHand.settled:
          # 'bet' is set to negative if we lost
          self.currentHandBalance += currentHand.bet

  def settle(self, dealerValue):
    for h in self.hands_:
      if not h.settled:
        h.settle(dealerValue)
        # 'bet' is set to negative if we lost
        self.currentHandBalance += h.bet

    self.balance += self.currentHandBalance
    if self.currentHandBalance > 0:
      logging.debug("next state is {state}".format(state=self.bettingState["next_win"]))
      self.bettingState = self.bettingStrategy[self.bettingState["next_win"]]
    elif self.currentHandBalance < 0:
      logging.debug("next state is {state}".format(state=self.bettingState["next_loss"]))
      self.bettingState = self.bettingStrategy[self.bettingState["next_loss"]]
    else:
      logging.debug("leaving state alone")
    self.currentHandBalance = 0.0

  def settleDealerBJ(self):
    # TODO: insurance?
    assert(len(self.hands_)==1)
    assert(self.hands_[0].cardCount() == 2)
    self.hands_[0].settle(21)
    self.currentHandBalance += self.hands_[0].bet

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

  def setPlayers(self, playerStrategyList, playerBettingStrategyList):
    self.playerStates = [playerstate(x, y) for x,y in zip(playerStrategyList, playerBettingStrategyList)]

  @staticmethod
  def dealCard_(deck, f, wantedValue):
    if wantedValue is None:
      f(deck.dealone())
    else:
      f(cards.card(wantedValue, 0))

  def playHand(self, dealerUpCard=None, playerFirstCard=None, playerSecondCard=None):
    # by rule, if there are less than two decks left, we reshuffle
    newShoe = self.deck.getCardCount() < 104
    if newShoe:
      self.deck.shuffle()

    # start new hands
    for s in self.playerStates:
      s.startNewHand(newShoe)
    self.dealerHand = bjhand()

    # deal first card to everyone
    for s in self.playerStates:
      self.dealCard_(self.deck, s.dealCard, playerFirstCard)
    self.dealCard_(self.deck, self.dealerHand.addCard, dealerUpCard)

    # deal second card to everyone
    for s in self.playerStates:
      self.dealCard_(self.deck, s.dealCard, playerSecondCard)
    self.dealCard_(self.deck, self.dealerHand.addCard, None)

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
            dealerCard=None,
            playerCard1=None, playerCard2=None,
            loggingLevel=logging.WARNING):
  # just play one hand, printing details
  logging.basicConfig(level=loggingLevel)
  mytable = table(deckCount)
  bs1 = [bjstrategies.BET_SIMPLE for x in range(playerCount//2)]
  bs2 = [bjstrategies.BET_STREAK for x in range(playerCount//2)]
  mytable.setPlayers([bjstrategies.S1 for x in range(playerCount)], bs1+bs2)
  for i in range(handCount):
    mytable.playHand(dealerUpCard=dealerCard,
                     playerFirstCard=playerCard1,
                     playerSecondCard=playerCard2)
  print('balances: {}'.format(mytable))



def splittest(deckCount, playerCount, handCount,
              loggingLevel=logging.WARNING):
  # just play one hand, printing details
  logging.basicConfig(level=loggingLevel)
  bjplay.createDatabase('splittest.db')
  mytable = table(deckCount)
  mytable.setPlayers([bjstrategies.MISTER_SPLITTER for x in range(playerCount)])
  for i in range(handCount):
    mytable.playHand()
  print('balances: {}'.format(mytable))

def test1():
  runtest(8, 8, 5, loggingLevel=logging.DEBUG)

def test2():
  runtest(8, 8, 1000000)

def test3():
  runtest(8, 2, 1000000,
          dealerCard=1,
          playerCard1=10,
          playerCard2=7)

def stest1():
  splittest(8, 8, 1, loggingLevel=logging.DEBUG)

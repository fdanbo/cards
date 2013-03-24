#!/usr/local/bin/python3.3

import cards
import bjstrategies

import logging

BET_AMOUNT = 1.0

# returns 1 for aces
def cardvalue(card):
  if card.rank < 11:
    return card.rank
  else:
    return 10

class bjhand:
  def __init__(self):
    self.cards_ = []
    self.value_ = 0
    self.haveAce_ = False
    self.closed_ = False

  def __repr__(self):
    string = ' '.join(str(x) for x in self.cards_)
    if self.busted():
      string += ' BUST'
    else:
      string += ' ' + str(self.value())
      if self.soft():
        string += 's'
    return string

  def firstCard(self):
    return self.cards_[0]

  def hit(self, card):
    self.cards_.append(card)
    self.value_ += cardvalue(card)
    if card.rank == 1:
      self.haveAce_ = True
    if self.value() >= 21:
      self.closed_ = True

  def stand(self):
    self.closed_ = True

  def value(self):
    if self.haveAce_:
      return self.value_ if self.value_ > 11 else (self.value_+10)
    else:
      return self.value_

  def blackjack(self):
    return (len(self.cards_) == 2 and
            self.haveAce_ and
            self.value_ == 11)

  def soft(self):
    return self.haveAce_ and self.value_ < 12

  def busted(self):
    return self.value_ > 21

  def closed(self):
    return self.closed_

  def moveAllowed(self, move):
    if move == 'stand':
      return True
    elif move == 'hit':
      return not self.closed_
    elif move == 'double':
      return len(self.cards_)==2
    elif move == 'surrender':
      return len(self.cards_)==2
    elif move == 'split':
      # split is not yet supported
      return False
      return (len(self.cards_) == 2 and
              cardvalue(self.cards_[0]) == cardvalue(self.cards_[1]))

class playerhand:
  def __init__(self, bet, strategy):
    self.strategy_ = strategy
    self.settled_ = False
    self.bet_ = bet
    self.hand_ = bjhand()

  def __repr__(self):
    return str(self.balance_)

  def addcard(self, card):
    self.hand_.hit(card)

  def chooseMove(self, dealerUpCard):
    section = self.strategy_[cardvalue(dealerUpCard)]
    handKey = self.hand_.value()
    if self.hand_.soft():
      handKey = 's'+str(handKey)
    for move in section[handKey].split(','):
      if self.hand_.moveAllowed(move):
        return move
    return 'stand'

  def double(self, card):
    self.hand_.hit(card)
    self.hand_.stand()
    self.betAmount_ *= 2


class playerstate:
  def __init__(self, strategy):
    self.strategy_ = strategy
    self.balance_ = 0.0

  def __repr__(self):
    return str(self.balance_)

  def startNewHand(self, bet):
    self.hands_ = [bjhand(bet, self.strategy)]

  def handiter(self):
    return iter(self.hands_)

  def win(self):
    self.balance_ += self.betAmount_
    self.settled_ = True

  def bjwin(self):
    self.balance_ += 1.5*self.betAmount_
    self.settled_ = True

  def lose(self):
    self.balance_ -= self.betAmount_
    self.settled_ = True

  def surrender(self):
    self.balance_ -= (self.betAmount_ / 2.0)
    self.settled_ = True

  def push(self):
    self.settled_ = True

  def settled(self):
    return self.settled_

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

    # first give one card to each of the players, give face-up card to dealer, then give another
    # card to each of the players, then give face-down card to dealer
    for s in self.playerStates: s.hand().hit(self.deck.dealone())
    self.dealerHand.hit(self.deck.dealone())
    for s in self.playerStates: s.hand().hit(self.deck.dealone())
    self.dealerHand.hit(self.deck.dealone())

    # now have everyone play their hands. this settles hands that busted, got blackjack, or lost to
    # a blackjack.
    for s in self.playerStates:
      self.playTurn_(s)
    self.playDealerTurn_()

    dealerValue = self.dealerHand.value()
    dealerBusted = self.dealerHand.busted()

    for s in self.playerStates:
      if not s.settled():
        playerValue = s.hand().value()
        if dealerBusted or playerValue > dealerValue:
          s.win()
        elif playerValue == dealerValue:
          s.push()
        else:
          s.lose()


  def playTurn_(self, playerstate):
    hand = playerstate.hand()

    # check for dealer blackjack
    if self.dealerHand.blackjack():
      # TODO: insurance
      # also note that these methods will both set the settled() bit on the player state, so the
      # while loop below will be skipped over.
      if hand.blackjack():
        playerstate.push()
      else:
        playerstate.lose()

    # check for player blackjack
    if hand.blackjack() and not playerstate.settled():
      playerstate.bjwin()

    # have the player play the hand
    while not (hand.closed() or hand.busted() or playerstate.settled()):
      move = playerstate.chooseMove(self.dealerHand.firstCard())
      if move == 'stand':
        hand.stand()
      elif move == 'hit':
        hand.hit(self.deck.dealone())
      elif move == 'double':
        playerstate.double(self.deck.dealone())
      elif move == 'surrender':
        playerstate.surrender()
      elif move == 'split':
        # to be implemented
        pass

      if hand.busted():
        # settles the hand so we'll break out of the loop
        playerstate.lose()

    logging.debug(hand)

  def playDealerTurn_(self):
    while self.dealerHand.value() < 17:
      self.dealerHand.hit(self.deck.dealone())
    logging.debug(self.dealerHand)


if __name__ == '__main__':
  N = 100000
  print('playing {} hands...'.format(N))

  # 8 decks, 8 players
  mytable = table(8)
  mytable.setPlayers([bjstrategies.S1 for x in range(8)])

  for i in range(N):
    mytable.playHand()

  print 'balances: {}'.format(mytable)

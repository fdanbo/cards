
class bjhand:
  def __init__(self):
    self.cards_ = []
    self.value_ = 0
    self.haveAce_ = False

  def __repr__(self):
    string = ' '.join(str(x) for x in self.cards_)
    if self.value() > 21:
      string += ' BUST'
    else:
      string += ' ' + str(self.value())
      if self.soft():
        string += 's'
    return string

  # returns 1 for aces
  @staticmethod
  def cardvalue(card):
    if card.rank < 11:
      return card.rank
    else:
      return 10

  def firstCard(self):
    return self.cards_[0]

  def secondCard(self):
    return self.cards_[1]

  def cardCount(self):
    return len(self.cards_)

  def addCard(self, card):
    self.cards_.append(card)
    self.value_ += bjhand.cardvalue(card)
    if card.rank == 1:
      self.haveAce_ = True

  def value(self):
    if self.haveAce_:
      if self.value_ > 11:
        return self.value_
      else:
        return self.value_+10
    else:
      return self.value_

  def soft(self):
    return self.haveAce_ and self.value_ < 12

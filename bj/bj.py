
import csv

# TODO
# - ignore dealer & player blackjacks
# - one card on split aces
# - soft hands

# - compute odds overall

class bjhand():
    def __init__(self, cardCount=0, total=0, soft=False, splitable=True):
        self.cardCount_ = cardCount
        self.total_ = total
        self.soft_ = soft
        self.splitable_ = splitable

    def clone(self):
        return bjhand(self.cardCount_, self.total_,
                      self.soft_, self.splitable_)

    def addCard(self, card):
        self.cardCount_ += 1
        self.total_ += card
        if not self.soft_:
            self.soft_ = (card == 1)

    def isBlackjack(self):
        return self.cardCount_ == 2 and self.value() == 21

    def createSplit(self):
        return bjhand(cardCount=1,
                      total=self.total_/2,
                      soft=self.total_==2,
                      splitable=False)

    def getLegalMoves(self):
        moves = set()
        moves.add('stand')
        if self.value() < 21:
            moves.add('hit')
            if self.cardCount_ == 2:
                moves.add('surrender')
                moves.add('double')
                if self.splitable_ and self.valueIsSplitable_():
                    moves.add('split')
        return moves

    def valueIsSplitable_(self):
        # this doesn't check the number of cards or whether we've split into the hand; just whether
        # it's possible the have a spliable hand with this value.  eg, ace-ace is the only splitable
        # soft hand.
        if self.soft():
            return self.total_ == 2
        else:
            return self.total_>2 and self.total_ % 2 == 0

    def busted(self):
        return self.value() > 21

    def value(self):
        if self.soft():
            return self.total_ + 10
        else:
            return self.total_

    def soft(self):
        return self.total_ <= 11 and self.soft_


class OddsCalculator():
    # 8 decks
    cardCounts = { 1:32, 2:32, 3:32, 4:32, 5:32, 6:32, 7:32, 8:32, 9:32, 10:128 }

    def __init__(self):
        self.cachedAverages_hard = dict([(x, {}) for x in range(4, 21)])
        self.cachedAverages_soft = dict([(x, {}) for x in range(12, 22)])
        self.splitsBeingComputed_ = set()

    def cache_(self, playerHand, dealerHand, averages):
        if playerHand.soft():
            self.cachedAverages_soft[playerHand.value()][dealerHand.value()] = averages
        else:
            self.cachedAverages_hard[playerHand.value()][dealerHand.value()] = averages

    def lookupInCache_(self, playerHand, dealerHand):
        try:
            if playerHand.soft():
                return self.cachedAverages_soft[playerHand.value()][dealerHand.value()]
            else:
                return self.cachedAverages_hard[playerHand.value()][dealerHand.value()]
        except KeyError:
            return None

    @staticmethod
    def averageAcrossCards_(hand, f, noTens=False, noAces=False):
        numeratorForAverage = 0.0
        denominatorForAverage = 0.0
        for card, cardCount in OddsCalculator.cardCounts.iteritems():
            if card==1 and noAces: continue
            if card==10 and noTens: continue
            currentHand = hand.clone()
            currentHand.addCard(card)
            numeratorForAverage += (f(currentHand)*cardCount)
            denominatorForAverage += cardCount
        return numeratorForAverage/denominatorForAverage

    def computeAverage_playerTurn(self, playerHand, dealerHand):
        legalMoves = playerHand.getLegalMoves()
        if 'hit' in legalMoves:
            averages = self.computeAverages_playerTurn(playerHand, dealerHand)
            return max([avg for move, avg in averages.iteritems() if move in legalMoves])
        else:
            return self.computeAverage_dealerTurn(playerHand, dealerHand)

    def computeAverages_playerTurn(self, playerHand, dealerHand):
        # check the cache
        averages = self.lookupInCache_(playerHand, dealerHand)
        if averages: return averages

        averages = {}

        # split. we do the split first, because recursing will automatically compute the rest of the
        # odds for us. to prevent an infinite loop, we only compute the split odds themselves at the
        # top level.
        def splitf(hand):
            return self.computeAverage_playerTurn(hand, dealerHand)
        # aces get only one card
        def splitf_aces(hand):
            return self.computeAverage_dealerTurn(hand, dealerHand)

        splitKey = (playerHand.value(), playerHand.soft(), dealerHand.value())
        if (playerHand.valueIsSplitable_() and
            splitKey not in self.splitsBeingComputed_):

            # note that the value being added is the hand value, ie 16 for splitting 8's
            self.splitsBeingComputed_.add(splitKey)

            splitHand = playerHand.createSplit()

            # because the odds don't change between the two hands, we just double the odds of one of
            # them.
            f = splitf_aces if playerHand.soft() else splitf
            splitAverage = 2.0*OddsCalculator.averageAcrossCards_(splitHand, f)

            # we expect the recursion to have computed the other odds for us, and cached them.  take
            # that and add the split odds to it.  The if is for testing, allows for not all of the
            # cards being in the deck.
            cachedAverages = self.lookupInCache_(playerHand, dealerHand)
            if cachedAverages:
                cachedAverages['split'] = splitAverage
                return cachedAverages
            else:
                averages['split'] = splitAverage

        # stand -- go straight to the dealer turn
        averages['stand'] = self.computeAverage_dealerTurn(playerHand, dealerHand)

        # hit
        def hitf(hand):
            if hand.busted():
                return -1.0
            else:
                return self.computeAverage_playerTurn(hand, dealerHand)
        averages['hit'] = OddsCalculator.averageAcrossCards_(playerHand, hitf)

        # surrender
        averages['surrender'] = -.5

        # double
        def doublef(hand):
            if hand.busted():
                return -2.0
            else:
                # double the bet and go straight to the dealer turn
                return 2.0*self.computeAverage_dealerTurn(hand, dealerHand)
        averages['double'] = OddsCalculator.averageAcrossCards_(playerHand, doublef)

        self.cache_(playerHand, dealerHand, averages)
        return averages


    def computeAverage_dealerTurn(self, playerHand, dealerHand):
        mustHit = dealerHand.value() < 17
        if dealerHand.soft() and dealerHand.value() == 17:
            mustHit = True

        def dealerf(hand):
            if hand.busted():
                return 1.0
            else:
                return self.computeAverage_dealerTurn(playerHand, hand)

        if mustHit:
            # do not consider dealer having blackjack as a possibility (since there is no
            # decision to be made in this case)
            noTens = dealerHand.cardCount_==1 and dealerHand.value() == 11
            noAces = dealerHand.cardCount_==1 and dealerHand.value() == 10
            return self.averageAcrossCards_(dealerHand, dealerf, noTens, noAces)
        else:
            if dealerHand.value() > playerHand.value():
                return -1.0
            elif dealerHand.value() == playerHand.value():
                return 0.0
            else:
                return 1.0

def test1():
    # two cards, sum=19
    playerHand = bjhand(2, 19)
    # one cards, sum=6
    dealerHand = bjhand(1, 6)

    calc = OddsCalculator()
    average = calc.computeAverage_dealerTurn(playerHand, dealerHand)
    print('average standing on 19 against a 6: {avg:.4f}'.format(avg=average))

def test2():
    # two cards, sum=20
    playerHand = bjhand(2, 20)
    # one card, sum=6
    dealerHand = bjhand(1, 6)

    calc = OddsCalculator()

    print('computing averages for 20 against a 6...')
    averages = calc.computeAverages_playerTurn(playerHand, dealerHand)

    for key, value in sorted(averages.iteritems()):
        print('{move}: {average:.4f}'.format(move=key, average=value))

def test3():
    # two cards, sum=2
    playerHand = bjhand(2, 2, soft=True)
    # one card, sum=1, soft (ie dealer has an ace)
    dealerHand = bjhand(1, 1, soft=True)

    calc = OddsCalculator()

    print('computing averages for 20 against an ace...')
    averages = calc.computeAverages_playerTurn(playerHand, dealerHand)

    for key, value in sorted(averages.iteritems()):
        print('{move}: {average:.4f}'.format(move=key, average=value))


def abbreviate_(move):
    if move=='hit': return 'H'
    if move=='stand': return 'S'
    if move=='surrender': return 'R'
    if move=='double': return 'D'
    if move=='split': return 'P'
    return '?'

def computeAndWrite(calc, playerHand, dealerHand, csvwriter):
    # compute
    averages = calc.computeAverages_playerTurn(playerHand, dealerHand)
    playerHandString = '{value}{soft}'.format(value=playerHand.value(),
                                              soft='s' if playerHand.soft() else '')
    csvwriter.writerow([dealerHand.value(), playerHandString,
                        averages.get('hit', 'n/a'),
                        averages.get('stand', 'n/a'),
                        averages.get('surrender', 'n/a'),
                        averages.get('double', 'n/a'),
                        averages.get('split', 'n/a')])

    # sort highest to lowest
    averages = sorted([(averages.get(move, -2.0), abbreviate_(move))
                        for move in ['hit', 'stand', 'surrender', 'double', 'split']],
                      reverse=True)
    # the string result is the order of the moves you want, but always ends if you run into a hit or
    # stand.
    resultString = ''
    for avg, move in averages:
        resultString += move
        if move=='H' or move=='S':
            break
    return resultString


def run():
    with open('raw.csv', 'w') as f1, open('collated.csv', 'w') as f2:
        csvwriter1 = csv.writer(f1)
        csvwriter2 = csv.writer(f2)

        csvwriter1.writerow(['dealer','player','hit','stand','surrender','double','split'])
        csvwriter2.writerow(['player','A','2','3','4','5','6','7','8','9','10'])

        calc = OddsCalculator()

        # for each possible hard player hand
        for pc in range(4, 21):
            print('player has: {card}'.format(card=pc))
            playerHand = bjhand(2, pc)

            resultStrings = []

            # for each possible dealer card
            for dc in range(2, 11) + [1]:
                print('  dealer has: {card}'.format(card=dc))
                dealerHand = bjhand(1, dc)
                resultStrings.append(computeAndWrite(calc, playerHand, dealerHand, csvwriter1))

            csvwriter2.writerow([playerHand.value()] + resultStrings)

        # for each possible soft player hand
        for pc in range(2, 11):
            print('player has: {card}s'.format(card=(pc+10)))
            playerHand = bjhand(2, pc, soft=True)

            # for each possible dealer card
            for dc in range(2, 11) + [1]:
                print('  dealer has: {card}'.format(card=dc))
                dealerHand = bjhand(1, dc)
                resultStrings.append(computeAndWrite(calc, playerHand, dealerHand, csvwriter1))

            csvwriter2.writerow([str(playerHand.value())+'s'] + resultStrings)

def profile():
    import cProfile
    cProfile.run('run()')

if __name__ == '__main__':
    run()

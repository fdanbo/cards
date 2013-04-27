
import csv
import functools
import multiprocessing

class bjhand():
    def __init__(self, cardCount=0, total=0, haveAce=False, splitable=True):
        self.cardCount_ = cardCount
        self.total_ = total
        self.haveAce_ = haveAce
        self.splitable_ = splitable

    def clone(self):
        return bjhand(self.cardCount_, self.total_,
                      self.haveAce_, self.splitable_)

    def addCard(self, card):
        self.cardCount_ += 1
        self.total_ += card
        if not self.haveAce_:
            self.haveAce_ = (card == 1)

    def isBlackjack(self):
        return self.cardCount_ == 2 and self.value() == 21

    def createSplit(self):
        return bjhand(cardCount=1,
                      total=self.total_/2,
                      haveAce=self.total_==2,
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

    def tostring(self):
        if self.cardCount_==1:
            return 'A' if self.total_==1 else str(self.total_)
        else:
            return '{value}{soft}'.format(value=self.value(),
                                          soft='s' if self.soft() else '')

    def soft(self):
        return self.total_ <= 11 and self.haveAce_


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


class OverallOddsCalculator():
    def __init__(self):
        self.calc = OddsCalculator()

    def computeOverallOdds(self):
        return OddsCalculator.averageAcrossCards_(bjhand(),
                                                  functools.partial(self.onFirstPlayerCard_, bjhand()))

    def onFirstPlayerCard_(self, dealerHand, playerHand):
        return OddsCalculator.averageAcrossCards_(dealerHand,
                                                  functools.partial(self.onFirstDealerCard_, playerHand))

    def onFirstDealerCard_(self, playerHand, dealerHand):
        return OddsCalculator.averageAcrossCards_(playerHand,
                                                  functools.partial(self.onSecondPlayerCard_, dealerHand))

    def onSecondPlayerCard_(self, dealerHand, playerHand):
        print('player has: {value}'.format(value=playerHand.value()))
        return OddsCalculator.averageAcrossCards_(dealerHand,
                                                  functools.partial(self.onSecondDealerCard_, playerHand))

    def onSecondDealerCard_(self, playerHand, dealerHand):
        print('  dealer has: {value}'.format(value=dealerHand.value()))

        # check for blackjack
        dealerHasBlackjack = dealerHand.isBlackjack();
        playerHasBlackjack = playerHand.isBlackjack();
        if dealerHasBlackjack:
            return 0.0 if playerHasBlackjack else -1.0
        elif playerHasBlackjack:
            return 1.5

        return self.calc.computeAverage_playerTurn(playerHand, dealerHand)

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
    playerHand = bjhand(2, 2, haveAce=True)
    # one card, sum=1, soft (ie dealer has an ace)
    dealerHand = bjhand(1, 1, haveAce=True)

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

def playerHardHands_():
    minTotal = 4
    maxTotal = 20
    return [bjhand(2, value) for value in range(minTotal, maxTotal+1)]

def playerSoftHands_():
    minTotal = 2
    maxTotal = 10
    return [bjhand(2, value, haveAce=True) for value in range(minTotal, maxTotal+1)]

def dealerHands_():
    minTotal = 2
    maxTotal = 10
    return [bjhand(1, value, haveAce=(value==1)) for value in range(minTotal, maxTotal+1) + [1]]

def computeOddsForDealerHand(dealerHand):
    calc = OddsCalculator()

    averagesByHand = {}

    # for each possible hard player hand
    for playerHand in playerHardHands_():
        averagesByHand[playerHand.tostring()] = calc.computeAverages_playerTurn(playerHand, dealerHand)

    # for each possible soft player hand
    for playerHand in playerSoftHands_():
        averagesByHand[playerHand.tostring()] = calc.computeAverages_playerTurn(playerHand, dealerHand)

    print('done computing for: {card}'.format(card=dealerHand.tostring()))
    return (dealerHand.tostring(), averagesByHand)

def run():
    pool = multiprocessing.Pool(10)

    # start the processes
    result = pool.map_async(computeOddsForDealerHand, dealerHands_())

    # blocks until all the processes are done
    rawData = result.get()

    # now write the output
    with open('raw.csv', 'w') as f1:
        csvwriter = csv.writer(f1)
        csvwriter.writerow(['dealer','player','hit','stand','surrender','double','split'])
        # FIXME: iterate in sorted order
        for dealerHand, playerHands in rawData:
            # FIXME: iterate in sorted order
            for playerHand, averages in playerHands.iteritems():
                resultArray = [averages.get(move, 'n/a') for move in ['hit', 'stand', 'surrender', 'double', 'split']]
                csvwriter.writerow([dealerHand, playerHand] + resultArray)

    with open('collated.csv', 'w') as f2:
        # create a map dealerhand->playerhand->string
        results = {}

        for (dealerHand, playerHands) in rawData:
            results[dealerHand] = {}
            for playerHand, averages in playerHands.iteritems():
                averages = sorted([(averages.get(move, -2.0), abbreviate_(move))
                                   for move in ['hit', 'stand', 'surrender', 'double', 'split']],
                                  reverse=True)
                # the string result is the order of the moves you want, but always ends if you run
                # into a hit or stand.
                resultString = ''
                for avg, move in averages:
                    resultString += move
                    if move=='H' or move=='S':
                        break
                results[dealerHand][playerHand] = resultString

        csvwriter = csv.writer(f2)
        csvwriter.writerow(['player'] + [hand.tostring() for hand in dealerHands_()])

        playerHandList = [x.tostring() for x in (playerHardHands_() + playerSoftHands_())]
        for playerHand in playerHandList:
            csvwriter.writerow([playerHand] + [results[dh.tostring()][playerHand] for dh in dealerHands_()])

def run2():
    calc = OverallOddsCalculator()
    odds = calc.computeOverallOdds()
    print('overall odds: {odds}'.format(odds=odds))


def profile():
    import cProfile
    cProfile.run('run()')

if __name__ == '__main__':
    run()

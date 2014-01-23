
from bj import bjhand, OddsCalculator

import random

def musthit(hand):
    if hand.value() < 17:
        return True
    if hand.soft() and hand.value() == 17:
        return True
    return False

def recurseTotals(hand):
    numerators = {'17':0.0, '18':0.0, '19':0.0, '20':0.0, '21':0.0, 'busted':0.0}
    denominator = 0.0
    for card, cardCount in OddsCalculator.cardCounts.iteritems():
        if hand.cardCount_ == 1 and card==10:
            continue
        newHand = hand.clone()
        newHand.addCard(card)
        if newHand.busted():
            numerators['busted'] += cardCount
        elif musthit(newHand):
            n, d = recurseTotals(newHand)
            for k in numerators.keys():
                numerators[k] += (n[k]/d)*cardCount
        else:
            numerators[str(newHand.value())] += cardCount
        denominator += cardCount
    assert(sum(numerators.values())==denominator)
    return numerators, denominator

def compute():
    startingHand = bjhand(1, 1, True)
    numerators, denominator = recurseTotals(startingHand)
    for hand, numerator in sorted(numerators.iteritems()):
        print('{}: {:.2f}%'.format(hand, numerator/denominator*100.0))

def simulate():
    N = 100000
    counts = {'17':0.0, '18':0.0, '19':0.0, '20':0.0, '21':0.0, 'busted':0.0}
    for i in range(N):
        h = bjhand(1, 1, True)
        while musthit(h):
            if h.cardCount_ > 1:
                c = random.randint(1, 13)
                if c>10: c=10
            else:
                c = random.randint(1, 9)
            h.addCard(c)
        if h.busted():
            counts['busted']+=1
        else:
            counts[str(h.value())]+=1
    for hand, count in sorted(counts.iteritems()):
        print('{}: {:.2f}%'.format(hand, count/N*100.0))

if __name__ == '__main__':
    compute()
    simulate()

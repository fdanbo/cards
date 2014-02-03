#!/usr/bin/env python3

import cards
from poker import poker


def random_sample_hands():
    # generate two of each type
    lists = {k: [] for k in range(poker.Ranking.high_card,
                                  poker.Ranking.straight_flush+1)}
    while True:
        deck = cards.Deck()
        hand = cards.Hand(deck.dealn(7))
        ranking = poker.get_7_card_ranking(hand)
        if len(lists[ranking.ranking]) < 2:
            print('{} {}'.format(hand.pretty(), ranking))
            lists[ranking.ranking].append(hand)
        if all(len(l) == 2 for l in lists.values()):
            break

    return sum(lists.values(), [])

if __name__ == '__main__':
    hands = random_sample_hands()
    for hand in hands:
        print("('{}', '{}'".format(hand, poker.get_7_card_ranking(hand)))

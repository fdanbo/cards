#!/usr/bin/env python3

from poker.interactive import HoldEmInterpreter
from poker.poker import ranking


def main():
    interpreter = HoldEmInterpreter()
    interpreter.cmdloop()


def test_split3():
    hands_played = 0
    interpreter = HoldEmInterpreter()
    signal = [True]
    winnercount = [0]

    # keep going until we have a 3-way split pot
    def callback(event, index=None, amount=None):
        interpreter.holdem_callback(event, index, amount)
        if event == 'showdown':
            winnercount[0] = 0
        elif event == 'win':
            winnercount[0] += 1
            if winnercount[0] > 2:
                signal[0] = False

    interpreter.holdem.callback = callback
    while signal[0]:
        interpreter.onecmd('deal')
        while not interpreter.holdem.winners:
            interpreter.onecmd('call')
        hands_played += 1

    totalbank = 0
    for p in interpreter.holdem.players:
        totalbank += p.bank
        print('{}: {}'.format(p.name, p.bank))
    print('total: {}'.format(totalbank))

    return hands_played


def test_straight_flush():
    hands_played = 0
    interpreter = HoldEmInterpreter()
    signal = [True]

    # keep going until we see a straight flush
    def callback(event, index=None, amount=None):
        interpreter.holdem_callback(event, index, amount)
        if event == 'showdown':
            for ps in interpreter.holdem.players:
                if not ps.folded:
                    if ((ps.hand.get_ranking().ranking ==
                         ranking.straight_flush)):
                        signal[0] = False

    interpreter.holdem.callback = callback
    while signal[0]:
        interpreter.onecmd('deal')
        while not interpreter.holdem.winners:
            interpreter.onecmd('call')
        hands_played += 1

    for p in interpreter.holdem.players:
        print('{}: {}'.format(p.name, p.bank))

    return hands_played

if __name__ == '__main__':
    # hands_played = test_split3()
    # hands_played = test_straight_flush()
    # print('hands played: {}'.format(hands_played))
    main()


import cards
from poker import poker


class MoveNotAllowed(Exception):
    pass


class PlayerState:
    def __init__(self, index, name):
        self.index = index
        self.bank = 0
        self.bet_this_round = 0
        self.played_this_round = False
        self.folded = False
        self.hand = None
        self.name = name


class HoldEm:
    small_blind = 1
    big_blind = 2

    def __init__(self, playernames, callback):
        self.players = [PlayerState(i, name)
                        for i, name in enumerate(playernames)]
        self.dealer_button = -1
        self.pot = 0
        self.upcards = []
        self.next_to_act = None
        self.winners = None
        self.callback = callback
        self.playing_blinds = False
        self.deck = cards.deck()

    def nextfrom(self, i, increment=1):
        return (i+increment) % len(self.players)

    def nextfrom_notfolded(self, i):
        n = self.nextfrom(i)
        while self.players[n].folded:
            n = self.nextfrom(n)
        return n

    def all_folded(self):
        unfolded = [p for p in self.players if not p.folded]
        return len(unfolded) == 1

    def putmoneyin(self, amount,
                   is_small_blind=False, is_big_blind=False):
        # bet has to be at least amount owed
        ps = self.players[self.next_to_act]
        amount_owed = (self.total_bet_this_round - ps.bet_this_round)
        if amount < amount_owed:
            raise MoveNotAllowed()
        amount_raised = amount - amount_owed

        ps.bank -= amount
        ps.bet_this_round += amount
        self.pot += amount
        self.total_bet_this_round += amount_raised

        # this was either the small blind, big blind, a call, or a raise.
        if is_small_blind:
            self.callback('small_blind', self.next_to_act, amount)
        elif is_big_blind:
            self.callback('big_blind', self.next_to_act, amount)
        elif amount == 0:
            self.callback('check', self.next_to_act, amount)
        elif amount_raised == 0:
            self.callback('call', self.next_to_act, amount)
        elif amount_owed == 0:
            self.callback('bet', self.next_to_act, amount)
        else:
            self.callback('raise', self.next_to_act, amount_raised)

        self.on_turn_completed()

    def fold(self):
        ps = self.players[self.next_to_act]
        ps.folded = True
        self.callback('fold', self.next_to_act)
        self.on_turn_completed()

    def on_turn_completed(self):
        ps = self.players[self.next_to_act]
        ps.played_this_round = True

        # figure out who's next
        n = self.nextfrom_notfolded(self.next_to_act)

        if self.all_folded():
            # this player won since everyone folded
            self.declare_winners([n])
        elif (not self.players[n].played_this_round or
              self.players[n].bet_this_round < self.total_bet_this_round):
            # this player is the next to act
            self.next_to_act = n
            amount_owed = (self.total_bet_this_round -
                           self.players[n].bet_this_round)
            if not self.playing_blinds:
                self.callback('next_to_act', n, amount_owed)
        elif (len(self.upcards) == 0 and
              self.players[n] == self.get_player_bb() and
              self.total_bet_this_round == self.big_blind):
            # special case: big blind option
            self.next_to_act = n
            self.callback('option', n, 0)
        else:
            # everyone who's in is in; start the next round
            self.start_next_round()

    def declare_winners(self, indices):
        # we sort the indices starting after the button
        keyfn = lambda x: (x-self.dealer_button-1) % len(self.players)
        indices.sort(key=keyfn)

        shares = [self.pot // len(indices)] * len(indices)

        # distribute the remainder
        remainder = self.pot % len(indices)
        for i in range(remainder):
            shares[i] += 1

        for i, index in enumerate(indices):
            ps = self.players[index]
            ps.bank += shares[i]

        self.next_to_act = None
        self.winners = indices

        if len(indices) > 1:
            self.callback('split_pot')

        for i, index in enumerate(indices):
            self.callback('win', index, shares[i])

        self.callback('end')

    def showdown(self):
        # assemble the poker hand objects
        players = [p for p in self.players if not p.folded]
        for p in players:
            for c in self.upcards:
                p.hand.addcard(c)

        # now find the highest
        highest = [players[0]]
        for p in players[1:]:
            if p.hand.get_ranking() > highest[0].hand.get_ranking():
                highest = [p]
            elif (p.hand.get_ranking() ==
                  highest[0].hand.get_ranking()):
                highest.append(p)

        self.callback('showdown')
        self.declare_winners([p.index for p in highest])

    def start_next_round(self):
        if len(self.upcards) == 5:
            # the hand is over
            self.showdown()
        else:
            # burn one
            self.deck.deal()

            cards_to_deal = 1 if self.upcards else 3
            self.upcards.extend(self.deck.deal(cards_to_deal))

            self.next_to_act = self.nextfrom_notfolded(self.dealer_button)

            for ps in self.players:
                ps.played_this_round = False
                ps.bet_this_round = 0
            self.total_bet_this_round = 0

            cards_on_table = len(self.upcards)
            if cards_on_table == 3:
                self.callback('flop')
            elif cards_on_table == 4:
                self.callback('turn')
            else:
                self.callback('river')

            if not self.playing_blinds:
                self.callback('next_to_act', self.next_to_act, 0)

    def get_player_bb(self):
        index = self.nextfrom(self.dealer_button, 2)
        return self.players[index]

    def get_player_sb(self):
        index = self.nextfrom(self.dealer_button, 1)
        return self.players[index]

    def get_player(self, index):
        return self.players[index]

    def get_state(self):
        d = {'pot': self.pot,
             'hands': [ps.hand for ps in self.players],
             'board': self.upcards}
        if self.winners:
            d['winners'] = self.winners
        elif self.next_to_act is not None:
            ps = self.players[self.next_to_act]
            amount_owed = (self.total_bet_this_round - ps.bet_this_round)
            d['action'] = (self.next_to_act, amount_owed)
        return d

    def deal(self):
        self.deck.shuffle()

        self.pot = 0
        self.upcards = []
        self.winners = None

        self.dealer_button = self.nextfrom(self.dealer_button)
        for ps in self.players:
            ps.hand = poker.hand()
            ps.folded = False
            ps.bet_this_round = 0
            ps.played_this_round = False

        self.total_bet_this_round = 0

        # deal two cards to each player
        for i in range(len(self.players)*2):
            # start with the dealer button and rotate
            r = self.nextfrom(self.dealer_button, i+1)
            self.players[r].hand.addcard(self.deck.dealone())

        # play the blinds
        self.next_to_act = self.nextfrom(self.dealer_button)
        self.playing_blinds = True
        self.putmoneyin(self.small_blind, is_small_blind=True)
        self.putmoneyin(self.big_blind, is_big_blind=True)
        self.playing_blinds = False
        self.callback('next_to_act', self.next_to_act, self.big_blind)

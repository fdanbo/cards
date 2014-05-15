
import cmd
import functools
import random
import termcolor

import poker.holdem as holdem
from poker.ai import HoldEmAI
from poker.poker import get_7_card_ranking


PLAYER_NAMES = ['dan-o'] + ['Player {}'.format(i) for i in range(1, 6)]


class display:
    def formatfn(fg=None, bg=None, attrs=None):
        def _format(s):
            return termcolor.colored(s, fg, bg, attrs)
        return _format

    name = formatfn(attrs=['bold'])
    amount = formatfn('magenta')
    bet = formatfn('green')
    _raise = formatfn('green')
    call = formatfn('yellow')
    check = formatfn('yellow')
    fold = formatfn('red')
    post = formatfn('green')
    cards = formatfn('blue', attrs=['bold'])


def wrap_command(f):
    @functools.wraps(f)
    def wrapped(self, line):
        try:
            f(self, line)
            self.act_until_player_turn()
        except holdem.MoveNotAllowed:
            if self.holdem.next_to_act is None:
                self.stdout.write(
                    'no hand is currently being played; try "deal".\n')
            else:
                self.stdout.write('that move is not currently allowed.\n')
    wrapped.unwrapped = f
    return wrapped


class HoldEmInterpreter(cmd.Cmd):
    prompt = '> '

    def __init__(self):
        cmd.Cmd.__init__(self)
        ais = [HoldEmAI(name) for name in PLAYER_NAMES]
        self.holdem = holdem.HoldEm(ais, self.holdem_callback)

    def holdem_callback(self, event, playerindex=None, amount=None):
        player_state = None
        if playerindex is not None:
            player_state = self.holdem.get_player(playerindex)

        if hasattr(self, 'event_{}'.format(event)):
            handler = getattr(self, 'event_{}'.format(event))
            handler(player_state, amount)

    def event_small_blind(self, player_state, amount):
        self.stdout.write('{} {posts} the small blind ({})\n'.format(
            display.name(player_state.name),
            display.amount(amount),
            posts=display.post('posts')))

    def event_big_blind(self, player_state, amount):
        self.stdout.write('{} {posts} the big blind ({})\n'.format(
            display.name(player_state.name),
            display.amount(amount),
            posts=display.post('posts')))

    def event_check(self, player_state, amount):
        self.stdout.write('{} {checks}.\n'.format(
            display.name(player_state.name),
            checks=display.check('checks')
        ))

    def event_bet(self, player_state, amount):
        self.stdout.write('{} {bets} {}.\n'.format(
            display.name(player_state.name),
            display.amount(amount),
            bets=display.bet('bets')))

    def event_call(self, player_state, amount):
        self.stdout.write('{} {calls} {}.\n'.format(
            display.name(player_state.name),
            display.amount(amount),
            calls=display.call('calls')))

    def event_raise(self, player_state, amount):
        self.stdout.write('{} {raises} {} to {}.\n'.format(
            display.name(player_state.name),
            display.amount(amount),
            display.amount(self.holdem.total_bet_this_round),
            raises=display._raise('raises')
        ))

    def event_fold(self, player_state, amount):
        self.stdout.write('{} {folds}.\n'.format(
            display.name(player_state.name),
            folds=display.fold('folds')))

    def event_next_to_act(self, player_state, amount):
        self.stdout.write('Pot: {} ({} players)\n'.format(
            display.amount(self.holdem.pot),
            self.holdem.count_unfolded()))
        if amount > 0:
            self.stdout.write('Action to {}; {} to call\n'.format(
                display.name(player_state.name),
                display.amount(amount)))
        else:
            self.stdout.write('Action to {}.\n'.format(
                display.name(player_state.name)))

    def event_option(self, player_state, amount):
        self.stdout.write('Option to {}.\n'.format(
            display.name(player_state.name)))

    def event_flop(self, player_state, amount):
        self.stdout.write('--------------------------------------------\n')
        self.stdout.write('DEALING THE FLOP!\n')
        board = ''.join([str(card) for card in self.holdem.upcards])
        self.stdout.write('[{}]\n'.format(display.cards(board)))

    def event_turn(self, player_state, amount):
        self.stdout.write('--------------------------------------------\n')
        self.stdout.write('DEALING THE TURN!\n')
        board = ''.join([str(card) for card in self.holdem.upcards])
        self.stdout.write('[{}]\n'.format(display.cards(board)))

    def event_river(self, player_state, amount):
        self.stdout.write('--------------------------------------------\n')
        self.stdout.write('DEALING THE RIVER!\n')
        board = ''.join([str(card) for card in self.holdem.upcards])
        self.stdout.write('[{}]\n'.format(display.cards(board)))

    def event_showdown(self, player_state, amount):
        self.stdout.write('--------------------------------------------\n')
        self.stdout.write('SHOWDOWN!\n')
        # show what everyone had
        for ps in self.holdem.players:
            if not ps.folded:
                self.stdout.write('{} had [{}{}] -- {}\n'.format(
                    display.name(ps.name),
                    display.cards(ps.hand[0]),
                    display.cards(ps.hand[1]),
                    display.cards(get_7_card_ranking(ps.hand))
                ))

    def event_split_pot(self, player_state, amount):
        # we'll get a separate 'win' callback for each
        self.stdout.write('split pot! total pot: {}\n'.format(
            display.amount(self.holdem.pot)))

    def event_win(self, player_state, amount):
        self.stdout.write('{} wins {}!\n'.format(
            display.name(player_state.name), display.amount(amount)))

    def event_end(self, player_state, amount):
        self.stdout.write('--------------------------------------------\n')

    def emptyline(self):
        return False

    def do_EOF(self, line):
        self.stdout.write('\n')
        return True

    def ai_action(self):
        amount_owed = self.holdem.get_amount_owed()
        if amount_owed > 0:
            # call most of the time
            possible_moves = ['fold', 'call', 'call', 'call', 'raise']
        else:
            # check most of the time
            possible_moves = ['check', 'check', 'check', 'bet']
        move = random.choice(possible_moves)

        # call the unwrapped command function for this move
        getattr(self, 'do_'+move).unwrapped(self, '')

    def act_until_player_turn(self):
        while True:
            if self.holdem.winners is not None:
                break
            else:
                if self.holdem.next_to_act > 0:
                    self.ai_action()
                else:
                    handstr = display.cards('[{}{}]'.format(
                        self.holdem.players[0].hand[0],
                        self.holdem.players[0].hand[1]))
                    self.stdout.write('You have: {}\n'.format(handstr))
                    break

    def do_deal(self, line):
        '''start a new hand'''
        self.stdout.write('--------------------------------------------\n')
        self.stdout.write('DEALING!\n')
        self.holdem.deal()
        self.act_until_player_turn()

    def do_players(self, line):
        '''show the list of players, along with their balances'''
        for player_state in self.holdem.players:
            self.stdout.write('{}: {}\n'.format(
                display.name(player_state.name),
                display.amount(player_state.bank)
            ))

    @wrap_command
    def do_fold(self, line):
        '''fold your hand.'''
        self.holdem.fold()

    @wrap_command
    def do_check(self, line):
        '''check—that is, don't bet anything.'''
        self.holdem.putmoneyin(0)

    @wrap_command
    def do_call(self, line):
        '''call the current bet.'''
        amount_owed = self.holdem.get_amount_owed()
        self.holdem.putmoneyin(amount_owed)

    @wrap_command
    def do_bet(self, line):
        '''place a bet.  the bet amount is the same as the big blind.'''
        self.holdem.putmoneyin(self.holdem.big_blind)

    @wrap_command
    def do_raise(self, line):
        '''raise by the big blind'''
        amount_owed = self.holdem.get_amount_owed()
        self.holdem.putmoneyin(amount_owed + self.holdem.big_blind)


import cmd
import random

import poker.holdem as holdem


class InvalidMove(Exception):
    pass


class HoldEmInterpreter(cmd.Cmd):
    prompt = '> '

    def __init__(self):
        cmd.Cmd.__init__(self)
        playernames = ['Player {}'.format(i) for i in range(6)]
        playernames[0] = 'dan-o'
        self.holdem = holdem.HoldEm(playernames, self.holdem_callback)

    def holdem_callback(self, event, playerindex=None, amount=None):
        if playerindex is not None:
            ps = self.holdem.get_player(playerindex)
        if event == 'small_blind':
            self.stdout.write('{} posts the small blind ({})\n'.format(
                ps.name, amount))
        elif event == 'big_blind':
            self.stdout.write('{} posts the big blind ({})\n'.format(
                ps.name, amount))
        elif event == 'check':
            self.stdout.write('{} checks.\n'.format(ps.name))
        elif event == 'bet':
            self.stdout.write('{} bets {}.\n'.format(ps.name, amount))
        elif event == 'call':
            self.stdout.write('{} calls {}.\n'.format(ps.name, amount))
        elif event == 'raise':
            self.stdout.write('{} raises {} to {}.\n'.format(
                ps.name, amount, self.holdem.total_bet_this_round
            ))
        elif event == 'fold':
            self.stdout.write('{} folds.\n'.format(ps.name))
        elif event == 'next_to_act':
            if amount > 0:
                self.stdout.write('Action to {}; {} to call\n'.format(
                    ps.name, amount))
            else:
                self.stdout.write('Action to {}.\n'.format(ps.name))
        elif event == 'option':
            self.stdout.write('Option to {}.\n'.format(ps.name))
        elif event == 'flop':
            self.stdout.write('--------------------------------------------\n')
            self.stdout.write('DEALING THE FLOP!\n')
            board = ' '.join([str(card) for card in self.holdem.upcards])
            self.stdout.write('[{} ]\n'.format(board))
        elif event == 'turn':
            self.stdout.write('--------------------------------------------\n')
            self.stdout.write('DEALING THE TURN!\n')
            board = ' '.join([str(card) for card in self.holdem.upcards])
            self.stdout.write('[{} ]\n'.format(board))
        elif event == 'river':
            self.stdout.write('--------------------------------------------\n')
            self.stdout.write('DEALING THE RIVER!\n')
            board = ' '.join([str(card) for card in self.holdem.upcards])
            self.stdout.write('[{} ]\n'.format(board))
        elif event == 'showdown':
            self.stdout.write('--------------------------------------------\n')
            self.stdout.write('SHOWDOWN!\n')
            # show what everyone had
            for ps in self.holdem.players:
                if not ps.folded:
                    self.stdout.write('{} had [{} {} ] -- {}\n'.format(
                        ps.name, ps.hand.cards[0], ps.hand.cards[1],
                        ps.hand.get_ranking()
                    ))
        elif event == 'split_pot':
            # we'll get a separate 'win' callback for each
            self.stdout.write('split pot! total pot: {}\n'.
                              format(self.holdem.pot))
        elif event == 'win':
            self.stdout.write('{} wins {}!\n'.format(ps.name, amount))
        elif event == 'end':
            self.stdout.write('--------------------------------------------\n')

    def emptyline(self):
        return False

    def do_EOF(self, line):
        self.stdout.write('\n')
        return True

    def ai_action(self, state):
        next_to_act, amount_owed = state['action']
        if amount_owed > 0:
            # call most of the time
            possible_moves = ['fold', 'call', 'call', 'call', 'raise']
        else:
            # check most of the time
            possible_moves = ['check', 'check', 'check', 'bet']
        move = random.choice(possible_moves)
        self.perform_move(state, move)

    def perform_move(self, state, move):
        try:
            next_to_act, amount_owed = state['action']
        except KeyError:
            self.stdout.write('no move is currently allowed. try "deal".\n')
            raise InvalidMove

        if move == 'fold':
            self.holdem.fold()
        elif move == 'check':
            self.holdem.putmoneyin(0)
        elif move == 'call':
            self.holdem.putmoneyin(amount_owed)
        elif move == 'bet':
            self.holdem.putmoneyin(2)
        elif move == 'raise':
            self.holdem.putmoneyin(amount_owed + 2)
        else:
            raise InvalidMove

    def act_until_player_turn(self):
        while True:
            state = self.holdem.get_state()
            if state.get('winners'):
                break
            else:
                action, amount_owed = state['action']
                if action != 0:
                    self.ai_action(state)
                else:
                    self.stdout.write('You have: [{} {} ]\n'.format(
                        self.holdem.players[0].hand.cards[0],
                        self.holdem.players[0].hand.cards[1],
                    ))
                    break

    def do_deal(self, line):
        '''start a new hand'''
        self.stdout.write('--------------------------------------------\n')
        self.stdout.write('DEALING!\n')
        self.holdem.deal()
        self.act_until_player_turn()

    def default(self, line):
        state = self.holdem.get_state()

        try:
            self.perform_move(state, line)
        except holdem.MoveNotAllowed:
            self.stdout.write('move not allowed: {}\n'.format(line))
        except InvalidMove:
            self.stdout.write('unknown move: {}\n'.format(line))
        else:
            self.act_until_player_turn()

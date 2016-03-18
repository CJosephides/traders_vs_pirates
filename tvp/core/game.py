"""
game.py

The Game and Game_State classes.

The Game class accepts players and acts as the main controller during play.

The Game_State class represents the state of play. Players use this to make
decisions about their actions during play.
"""

from .deck import Deck
from .player import Player_View

class Game:
    """
    The main controller for the game.
    Initializing assumes a new game without players, which must be added
    manually. Make sure that the players have a strategy before adding.
    """

    def __init__(self):
        self.turn = 0
        self.round_ = 0
        self.players = []
        self.scores = []
        self.idealer = None
    
    def add_player(self, player):
        if player in self.players:
            raise Exception('Player already in player list.')
        else:
            self.players.append(player)
            self.scores.append(0)

    def new_turn(self):
        
        # Other initialization pre-checks go here.
        # ...
        # e.g. check number of players

        # Reset player states.
        for player in self.players:
            player.hand = []
            player.public_commits = []
            player.private_commits = []

        # New list of game states.
        self.states = []

        # Update counters.
        self.round_ = 0
        self.turn += 1

        # Set dealer position.
        if self.idealer is None:
            self.idealer = 0
        else:
            self.idealer += 1
            if self.idealer == len(self.players):
                self.idealer = 0

        # Set up a player sequence starting from dealer.
        # TODO: Check that this is fine for idealer == 0.
        self.sequence = self.players[self.idealer:] + \
                        self.players[:self.idealer]

        # Set active player at dealer.
        self.iactive = self.idealer

        # Make new deck. 
        self.deck = Deck()

        # Start pool.
        self.pool = []

        # Deal three cards to each player.
        for player in self.players:
            for i in range(3):
                player.hand.append(self.deck.deal_card())

    def play_round(self):

        # Update counters.
        self.round_ += 1

        # Deal one card to the pool.
        self.pool.append(self.deck.deal_card())

        # For each player in the sequence.
        for iplayer, player in enumerate(self.sequence):

            # Keep track of active player index.
            self.iactive = iplayer

            # Make new game state, append to list.
            current_state = Game_State(self)
            self.states.append(current_state)

            # Request action from player.
            action = player.play(self.states)

            # Resolve action.
            self.resolve_action(player, action)

    def resolve_action(self, player, action):

        if action is None:
            # No card played: do nothing.
            pass
        else:
            if action[0] == 'i':
                # Investment card played.
                player.public_commits.append(action)
                player.hand.remove(action)
            else:
                # Security or piracy card played.
                player.private_commits.append(action)
                player.hand.remove(action)

    def end_turn(self, report=False):

        # Determine value of treasure.
        n_invest, v_invest = self.count_cards('i')
        treasure = n_invest * v_invest

        # Determine value of security.
        n_security, v_security = self.count_cards('s')

        # Determine value of piracy.
        n_piracy, v_piracy = self.count_cards('p')

        # Determine if pirates or traders win.
        if v_security == v_piracy:
            outcome = 'draw'
        elif v_security > v_piracy:
            outcome = 'trade'
        else:
            outcome = 'piracy'

        # Keep old player scores for deltas.
        old_scores = []
        for player in self.sequence:
            old_scores.append(player.score)

        # Give points to players from trading or pirating, depending on
        # outcome.
        for player in self.sequence:
            if outcome == 'draw':
                player.score += 0

            elif outcome == 'trade':
                player_v_invest = 0
                for card in player.public_commits:
                    if card[0] == 'i':
                        player_v_invest += int(card[1:])
                player.score += (n_invest * player_v_invest)

            elif outcome == 'piracy':
                player_n_piracy = 0
                for card in player.private_commits:
                    if card[0] == 'p':
                        player_n_piracy += 1
                player.score += round(
                    (float(player_n_piracy) / float(n_piracy)) * treasure)

        # Give points to player for keeping resources.
        for player in self.sequence:
            for card in player.hand:
                player.score += int(card[1:])

        # Give points to players from successful security.
        if outcome == 'trade':
            for player in self.sequence:
                player_v_security = 0
                for card in player.private_commits:
                    if card[0] == 's':
                        player_v_security += int(card[1:])

                player.score += player_v_security

        # Give penalties to players from failed piracy.
        for player in self.sequence:

            if outcome == 'trade':
                player_v_piracy = 0
                for card in player.private_commits:
                    if card[0] == 'p':
                        player_v_piracy += int(card[1:])
                player.score -= player_v_piracy

        # Report, if requested.
        if report:
            print('Turn %d report. ' % self.turn)
            print('Treasure value = %d (number = %d, value = %d).' %
                  (treasure,
                   n_invest,
                   v_invest))
            print('Security value = %d (number = %d).' %
                  (v_security,
                   n_security))
            print('Piracy value = %d (number = %d).' %
                  (v_piracy,
                   n_piracy))
            print('Outcome = %s.' % outcome)
            for iplayer, player in enumerate(self.sequence):
                print('%s score = %d (turn delta = %d).'
                      % (player.name,
                         player.score,
                         player.score - old_scores[iplayer]))
            print('===\n')

    def count_cards(self, card_type):

        n_cards = 0
        v_cards = 0

        # # Check pool.
        for card in self.pool:
            if card[0] == card_type:
                n_cards += 1
                v_cards = int(card[1:])

        # # Check players.
        for player in self.sequence:
            for card in player.public_commits:
                if card[0] == card_type:
                    n_cards += 1
                    v_cards += int(card[1:])
            for card in player.private_commits:
                if card[0] == card_type:
                    n_cards += 1
                    v_cards += int(card[1:])

        return n_cards, v_cards

    # def summarize_state(self):

    #     # Do some calculations.
    #     n_invest, v_invest = self.count_cards('i')
    #     treasure = n_invest * v_invest

    #     # Determine value of security.
    #     n_security, v_security = self.count_cards('s')

    #     # Determine value of piracy.
    #     n_piracy, v_piracy = self.count_cards('p')

    #     print('Turn = %d, Round = %d' % (self.turn, self.round_))
    #     print('----')
    #     print('Pool: %s' % str(self.pool))
    #     for player in self.sequence:
    #         print('%s -- public: %s, private: %s, in hand: %s, score: %d.' % 
    #               (player.name,
    #                str(player.public_commits),
    #                str(player.private_commits),
    #                str(player.hand),
    #                player.score
    #                ))
    #     print('----')
    #     print('Treasure value = %d (number = %d, value = %d).'
    #           % (treasure, n_invest, v_invest))
    #     print('Security value = %d.' % v_security)
    #     print('Piracy value = %d.' % v_piracy)
    #     print('')

    def play_turn(self, report=False):

        self.new_turn()
        self.play_round()
        self.play_round()
        self.play_round()
        self.end_turn(report=report)

    def play_game(self, n_turns):

        # Memory for time-series scores.
        ts_scores = {p.name: [] for p in self.players}

        # Play n_turns.
        for t in range(n_turns):
            self.play_turn(report=False)
            for player in self.players:
                ts_scores[player.name].append(player.score)

        # Generate (final) game result and timeseries result.
        result = []
        result_ts = []

        # Get information for each player.
        for player in self.players:
            result.append(
                {'name': player.name,
                 'score': ts_scores[player.name][-1],
                 'strategy': player.strategy.name}
            )
            result_ts.append(
                {'name': player.name,
                 'scores': ts_scores[player.name],
                 'strategy': player.strategy.name}
            )

        self.result = result
        self.result_ts = result_ts


class Game_State:
    """
    The game state represents a snapshot of the game. It is typically used for
    making player-side reports and for player decisions.
    """

    def __init__(self, game):
        self.round_ = game.round_
        self.turn = game.turn
        self.sequence = [p.name for p in game.sequence]
        self.idealer = game.idealer
        self.iactive = game.iactive
        self.pool = game.pool.copy()
        self.views = [Player_View(p) for p in game.sequence]



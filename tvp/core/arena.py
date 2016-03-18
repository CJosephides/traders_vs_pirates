"""
arena.py

Compete strategies against each other over many games.
"""

import random

from .game import Game
from .player import Player


class Pit:
    """
    Compete a set of strategies over many games. Unlike the Arena class, this
    does not use a random assortment of strategies for each game. Note that if
    we want multiple players to have the same strategy, we should add the
    strategy multiple times in the 'compete_strats' argument.
    """

    def __init__(self, compete_strats):
        self.compete_strats = compete_strats

    def run(self, n_turns, n_games, output=False):

        if output:
            print('Running games: ', end='')

        # Allocate memory for outcomes.
        outcomes = []

        # Play n_games.
        for ig in range(n_games):
            # Initialize game.
            game = Game()
            # Create players.
            for ip in range(len(self.compete_strats)):
                player = Player(name='%d' % ip)
                player.set_strategy(self.compete_strats[ip])
                game.add_player(player)

            # Play the game and return result time series.
            game.play_game(n_turns=n_turns)
            outcomes.append(game.result_ts)
            if output:
                print('.', end='')

        self.outcomes = outcomes

        if output:
            print(' done.')


class Arena:
    """
    Compete a set of strategies against random assortments over many games.
    """

    def __init__(self,
                 compete_strategies,
                 n_games,
                 n_turns,
                 n_players):

        self.compete_strategies = compete_strategies
        self.n_games = n_games
        self.n_turns = n_turns
        self.n_players = n_players

    def run(self):

        # Allocate memory for outcomes.
        outcomes = []

        # Play n_games.
        for ig in range(self.n_games):

            game = Game()
            # Create the players.
            for ip in range(self.n_players):
                # Choose a random strategy from the set of competing
                # strategies.
                # NOTE: We are not expecting strategy parameters.
                strat = random.choice(self.compete_strategies)
                player = Player(name='player_%d' % ig)
                player.set_strategy(strat)
                game.add_player(player)  # by reference

        

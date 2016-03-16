"""
player.py

The Player and Player_View classes.
"""

class Player:
    """
    A player object that can participate in a game. Don't forget to
    set_strategy after initializing.
    """

    def __init__(self, name=None):
        self.name = name
        self.score = 0.

        self.hand = []
        self.public_commits = []
        self.private_commits = []

    def set_strategy(self, strategy):
        self.strategy = strategy

    def play(self, game_state):
        return self.strategy.play(game_state, self)


class Player_View():
    """
    A player object, as would appear to another player -- i.e. with the content
    private commits obscured, but their number known.
    """

    def __init__(self, player):
        self.name = player.name
        self.n_hand = len(player.hand)
        self.n_private_commits = len(player.private_commits)
        self.public_commits = player.public_commits
        self.score = player.score

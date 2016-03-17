"""
strategy_null.py

author: Christos
date: 16/03/2016
description: never play
"""

class Strategy_Null:

    def __init__(self):
        self.name = 'null'

    def play(self, states, active_player):
        action = None
        return action

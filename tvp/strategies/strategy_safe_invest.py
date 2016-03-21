"""
strategy_safe_invest.py

author: Christos
date: 20/03/2016
description: invest strongest card only if the pool is safe
"""

import random

class Strategy_Safe_Invest:

    def __init__(self):
        self.name = 'safe_invest'

    def play(self, states, active_player):
        # Reference the current (latest) game state.
        gs = states[-1]

        # Count security and piracy in the pool.
        v_security = 0
        v_piracy = 0
        for card in gs.pool:
            if card[0] == 's':
                v_security += int(card[1:])
            elif card[0] == 'p':
                v_piracy += int(card[1:])

        # Do nothing if pool not safe.
        if v_piracy > v_security:
            return None

        # Otherwise, play strongest investment card.
        best_v_invest = 0
        action = None
        for card in active_player.hand:
            if card[0] == 'i':
                if int(card[1:]) > best_v_invest:
                    best_v_invest = int(card[1:])
                    action = card

        return action

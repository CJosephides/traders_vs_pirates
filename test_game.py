import numpy as np
import matplotlib.pyplot as plt

from tvp.core import *
from tvp.strategies import *

p1 = Player('player1')
p2 = Player('player2')
p3 = Player('player3')
p4 = Player('player4')

p1.set_strategy(Strategy_Null())
p2.set_strategy(Strategy_Null())
# p3.set_strategy(Strategy_Null())
p3.set_strategy(Strategy_Random())
p4.set_strategy(Strategy_Random())

game = Game()
game.add_player(p1)
game.add_player(p2)
game.add_player(p3)
game.add_player(p4)

scores = []
for i in range(100):
    game.new_turn()
    game.play_round()
    game.play_round()
    game.play_round()
    # game.end_turn(report=True)
    game.end_turn(report=False)
    this_scores = []
    for p in game.players:
        this_scores.append(p.score)
    scores.append(this_scores)

scores = np.array(scores)

fig, ax = plt.subplots(1, 1)
for iplayer, player in enumerate(game.players):
    ax.plot(scores[:, iplayer], label=player.strategy.name)

ax.legend(loc='upper left')
plt.show()

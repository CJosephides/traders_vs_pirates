from tvp import core
from tvp import strategies
from tvp import viz

pit = core.Pit([strategies.Strategy_Null(),
                strategies.Strategy_Null(),
                strategies.Strategy_Random(),
                strategies.Strategy_Random()])

# pit = core.Pit([strategies.Strategy_Null(),
#                 strategies.Strategy_Null(),
#                 strategies.Strategy_Null(),
#                 strategies.Strategy_Random()])

pit.run(n_turns=100, n_games=10)
viz.plot_pit(pit)

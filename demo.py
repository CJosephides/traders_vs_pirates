from tvp import core
from tvp import strategies
from tvp import viz

# --- Naive strategies
# Performance of the 'random' strategy depends on the number of 'null'
# strategies.

# pit = core.Pit([strategies.Strategy_Null(),
#                 strategies.Strategy_Random(),
#                 strategies.Strategy_Random(),
#                 strategies.Strategy_Random()])

# pit = core.Pit([strategies.Strategy_Null(),
#                 strategies.Strategy_Null(),
#                 strategies.Strategy_Random(),
#                 strategies.Strategy_Random()])

# pit = core.Pit([strategies.Strategy_Null(),
#                 strategies.Strategy_Null(),
#                 strategies.Strategy_Null(),
#                 strategies.Strategy_Random()])

# --- Pool strategies
# pit = core.Pit([strategies.Strategy_Null(),
#                 strategies.Strategy_Null(),
#                 strategies.Strategy_Null(),
#                 strategies.Strategy_Safe_Invest()])

# pit = core.Pit([strategies.Strategy_Null(),
#                 strategies.Strategy_Null(),
#                 strategies.Strategy_Safe_Invest(),
#                 strategies.Strategy_Safe_Invest()])

pit = core.Pit([strategies.Strategy_Null(),
                strategies.Strategy_Null(),
                strategies.Strategy_Random(),
                strategies.Strategy_Safe_Invest()])


pit.run(n_turns=100, n_games=20)
viz.plot_pit(pit)

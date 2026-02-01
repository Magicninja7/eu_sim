import math
import copy
import sys
from pathlib import Path


# i have no idea what this does
# chatgpt wrote it
# but if i delete it, the code stops working
# soooooo
# dont delete
ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stavanger_app.web.CLI.chain_of_events.infra import policies, stats, types_of_stats, last_incrimentation
from logic import do_all


stats_copy = do_all(policies(), stats())
main_stats = stats()
las_increment = last_incrimentation()

typs = ['economy', 'inner_workings', 'diplomacy', 'human_rights', 'security', 'demographics', 'people']

print(stats_copy.security['crime_rate'])
print(main_stats.security['crime_rate'])

def go_thru():
    for typ in typs:
        for sta in types_of_stats[typ]:
            if getattr(stats_copy, typ)[sta] != getattr(main_stats, typ)[sta]:
                if getattr(las_increment, typ)[sta] == 0:
                    diff = getattr(main_stats, typ)[sta] - getattr(stats_copy, typ)[sta]
                    if diff > 0:
                        incr = -1
                    elif diff < 0:
                        incr = 1
                    getattr(las_increment, typ)[sta] = incr # if diff is zero, it will stay so
                    getattr(main_stats, typ)[sta] += incr

                else:
                    incr = getattr(las_increment, typ)[sta] * 1.5
                    if incr > 0:
                        if (getattr(main_stats, typ)[sta] + incr) > getattr(stats_copy, typ)[sta]:
                            getattr(las_increment, typ)[sta] = 0
                            getattr(main_stats, typ)[sta] = getattr(stats_copy, typ)[sta]
                        else:
                            getattr(main_stats, typ)[sta] += incr
                    else:
                        if (getattr(main_stats, typ)[sta] + incr) < getattr(stats_copy, typ)[sta]:
                            getattr(las_increment, typ)[sta] = 0
                            getattr(main_stats, typ)[sta] = getattr(stats_copy, typ)[sta]   
                        else:
                            getattr(main_stats, typ)[sta] += incr


if __name__ == "__main__":
    for i in range(6):
        go_thru()
        print(f'iteration {i}')
        print(stats_copy.security['crime_rate'])
        print(main_stats.security['crime_rate'])
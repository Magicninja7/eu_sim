from increment import go_thru

from stavanger_app.web.CLI.chain_of_events.infra import policies, stats, types_of_stats, last_incrimentation
from logic import do_all


stats_copy = do_all(policies(), stats())
main_stats = stats()
las_increment = last_incrimentation()


if __name__ == "__main__":
    for i in range(9):
        go_thru(main_stats, stats_copy, las_increment)
        print(f'iteration {i}')
        print(stats_copy.security['crime_rate'])
        print(main_stats.security['crime_rate'])
        print(las_increment.security['crime_rate'])

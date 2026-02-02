

def go_thru(main_stats, stats_togo, las_increment, types_of_stats):
    typs = ['economy', 'inner_workings', 'diplomacy', 'human_rights', 'security', 'demographics', 'people']
    for typ in typs:
        for sta in types_of_stats[typ]:
            if getattr(stats_togo, typ)[sta] != getattr(main_stats, typ)[sta]:
                if getattr(las_increment, typ)[sta] == 0:
                    diff = getattr(main_stats, typ)[sta] - getattr(stats_togo, typ)[sta]
                    if diff > 0:
                        incr = -1
                    elif diff < 0:
                        incr = 1
                    getattr(las_increment, typ)[sta] = incr # if diff is zero, it will stay so
                    getattr(main_stats, typ)[sta] += incr

                else:
                    incr = round(getattr(las_increment, typ)[sta] * 1.2, 1)
                    
                    if incr > 0:
                        if (getattr(main_stats, typ)[sta] + incr) < getattr(stats_togo, typ)[sta]:
                            getattr(las_increment, typ)[sta] = 0
                            getattr(main_stats, typ)[sta] = getattr(stats_togo, typ)[sta]
                        else:
                            getattr(main_stats, typ)[sta] = round(getattr(main_stats, typ)[sta] + incr, 2)
                            getattr(las_increment, typ)[sta] = incr
                    else:
                        if (getattr(main_stats, typ)[sta] + incr) < getattr(stats_togo, typ)[sta]:
                            getattr(las_increment, typ)[sta] = 0
                            getattr(main_stats, typ)[sta] = getattr(stats_togo, typ)[sta]   
                        else:
                            getattr(main_stats, typ)[sta] = round(getattr(main_stats, typ)[sta] + incr, 2)
                            getattr(las_increment, typ)[sta] = incr
    return main_stats, las_increment
                    
                    


if __name__ == "__main__":
    for i in range(6):
        go_thru()
        print(f'iteration {i}')
        print(stats_togo.security['crime_rate'])
        print(main_stats.security['crime_rate'])
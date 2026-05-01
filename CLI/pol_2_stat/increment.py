

def go_thru(main_stats, stats_togo, las_increment, types_of_stats):
    typs = ['economy', 'inner_workings', 'diplomacy', 'human_rights', 'security', 'demographics', 'people']
    for typ in typs:
        for sta in types_of_stats[typ]:
            current = getattr(main_stats, typ)[sta]
            target = getattr(stats_togo, typ)[sta]
            if target == current:
                getattr(las_increment, typ)[sta] = 0
                continue

            last = getattr(las_increment, typ)[sta]
            diff = target - current  # positive: need to go up; negative: need to go down

            # If the previous step was moving the wrong way (e.g. an event
            # flipped the target above current after we were drifting down),
            # restart from a unit step in the new direction.
            if last == 0 or (last > 0) != (diff > 0):
                incr = 1 if diff > 0 else -1
            else:
                incr = round(last * 1.2, 1)
                # keep the magnitude growing even when rounding stalls it
                if abs(incr) <= abs(last):
                    incr = round(last + (0.1 if last > 0 else -0.1), 1)

            # Snap to target when the next step would reach or overshoot it.
            if abs(incr) >= abs(diff):
                getattr(main_stats, typ)[sta] = target
                getattr(las_increment, typ)[sta] = 0
            else:
                getattr(main_stats, typ)[sta] = round(current + incr, 2)
                getattr(las_increment, typ)[sta] = incr
    return main_stats, las_increment
                    
                    
import warnings

import spack.solver.asp as asp

SOLUTION_PHASES = 'setup', 'load', 'ground', 'solve'


def process_single_item(inputs):
    args, specs, idx, cf, i = inputs
    try:
        sol_res, timer, len_pkgs, solve_stat = asp.solve(specs, timers=False, reuse=args.reuse, rtimer=True, coref=args.cores, conf=cf)
        timer.stop()
        time_by_phase = tuple(timer.phases[ph] for ph in SOLUTION_PHASES)
    except Exception as e:
        warnings.warn(str(e))
        return None
    return (specs[0].name, cf, i) +  time_by_phase + (timer.total, len_pkgs)

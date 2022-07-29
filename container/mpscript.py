import warnings
import signal

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


def timeout_handler(signum, frame):
    raise RuntimeError("Timeout reached, exiting function")

def process_single_item_old_concretizer(inputs):
    # Set a timeout after 10 mins. to avoid stalling on a few
    # specs with the old concretizer
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(600)
    args, specs, idx, i = inputs
    try:
        timer = specs[0]._old_concretize()
        timer.stop()
    except Exception as e:
        return (specs[0].name, specs[0].concrete, i, 0.0)
    return (specs[0].name, specs[0].concrete, i, timer.total)

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import argparse
import functools
import os
import sys

import resinf
import utilo

import gennex.rerun

PROCESS = 'gennex_regen'


@utilo.saveme
def main(generated=None):
    root = utilo.baw_root(os.getcwd())
    parser = create_parser()
    start, worker = parse_args(parser)
    if returncode := run(root, start, worker, generated=generated):
        return sys.exit(returncode)
    return sys.exit(utilo.SUCCESS)


def run(root, start, worker: int = 1, generated=None) -> int:
    if not generated:
        generated = resinf.generated(project=root)
    if not utilo.exists(generated):
        utilo.error(f'no resource generated: {generated}')
        return utilo.FAILURE
    todo = []
    for path in os.listdir(generated):
        path = os.path.join(generated, path, 'generated.log')
        if not os.path.exists(path):
            continue
        todo.append(functools.partial(single, path, start))
    if not todo:
        utilo.error(f'nothing todo: {generated}')
        return utilo.FAILURE
    utilo.fork(*todo, worker=worker)
    return utilo.SUCCESS


def single(logfile, start: int = 0):
    steps = gennex.rerun.parse_steps(logfile, start=start)
    logmsg = f'Steps: {len(steps)} Start: {start} {logfile}'
    utilo.log(logmsg)
    for _, step in steps:
        utilo.log(step)
        completed = utilo.run(cmd=step)
        if not completed.returncode:
            continue
        utilo.error(f'{logmsg}\n{completed.stderr}\n{completed.stdout}')


def parse_args(parser) -> tuple:
    args = vars(parser.parse_args())
    start = int(args.get('start', 0))
    worker = int(args.get('worker', 1))
    return start, worker


def create_parser():
    parser = argparse.ArgumentParser(prog=PROCESS)
    # TODO: ADD VERBOSE AND FAIL FAST FLAG
    parser.add_argument(
        'start',
        help='start with number',
        default='5',
    )
    parser.add_argument(
        'worker',
        help='number of parallel executor',
        nargs='?',
        default='1',
    )
    return parser

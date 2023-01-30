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
import utila

import genex.rerun

PROCESS = 'genex_regen'


@utila.saveme
def main(generated=None):
    root = determine_root(os.getcwd())
    parser = create_parser()
    start, worker = parse_args(parser)
    if returncode := run(root, start, worker, generated=generated):
        return sys.exit(returncode)
    return sys.exit(utila.SUCCESS)


def run(root, start, worker: int = 1, generated=None) -> int:
    if not generated:
        generated = resinf.generated(project=root)
    if not utila.exists(generated):
        utila.error(f'no resource generated: {generated}')
        return utila.FAILURE
    todo = []
    for path in os.listdir(generated):
        path = os.path.join(generated, path, 'generated.log')
        if not os.path.exists(path):
            continue
        todo.append(functools.partial(single, path, start))
    utila.fork(*todo, worker=worker)
    return utila.SUCCESS


def single(logfile, start: int = 0):
    steps = genex.rerun.parse_steps(logfile, start=start)
    logmsg = f'Steps: {len(steps)} Start: {start} {logfile}'
    utila.log(logmsg)
    for _, step in steps:
        utila.log(step)
        completed = utila.run(cmd=step)
        if not completed.returncode:
            continue
        utila.error(f'{logmsg}\n{completed.stderr}\n{completed.stdout}')


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


def determine_root(path) -> str:
    # STOLEN FROM BAW PROJECT
    current = str(path)
    while not os.path.exists(os.path.join(current, '.baw')):  # pylint:disable=W0149
        current, base = os.path.split(current)
        if not str(base).strip():
            return None
    return current

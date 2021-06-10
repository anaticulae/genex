# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila
import utilatest

import genex


def extract_removepages(
    resources,
    dest=None,
    removepages: str = '1:3',
    folder: str = 'notoc',
    worker: str = 8,
    **kwargs,
):
    dest = power.generated(folder=folder) if not dest else dest
    files = [
        item[0] if not isinstance(item, str) else item for item in resources
    ]
    # prepare
    without_titlepage = [
        os.path.join(dest, f'{item}.pdf')
        for item in utilatest.simplify_testfile_names(
            files + [power.REPOSITORY],  # ensure correct parent
            sort=False,
        )
    ]
    # jam
    todo = []
    for inpath, outpath in zip(files, without_titlepage):
        todo.append(f'jam -i {inpath} -o {outpath} --remove={removepages}')
    # generate
    for job, _ in genex.todolist(
            without_titlepage + [dest],  # ensure correct parent
            dest,
            **kwargs,
    ):
        job = ' && '.join(job)
        todo.append(job)
    # avoid race condition that jam is not ready before starting extraction
    worker = utila.mins(len(files), worker)
    utila.run_parallel(todo, worker=worker)

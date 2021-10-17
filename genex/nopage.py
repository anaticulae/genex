# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import power
import utila

import genex
import genex.config


def extract_removepages(
    resources,
    dest=None,
    removepages: str = '1:3',
    folder: str = 'notoc',
    worker: str = 8,
    **kwargs,
):
    # CLEAN UP THIS HACK Y PLACE
    dest = power.generated(folder=folder) if not dest else dest
    files = [
        item[0] if not isinstance(item, str) else item for item in resources
    ]
    # prepare
    without_titlepage = [
        os.path.join(dest, f'{genex.config.simple(item)}.pdf') for item in files
    ]
    # TODO: USE GHOST?
    # jam
    todo = []
    for inpath, outpath in zip(files, without_titlepage):
        todo.append(
            functools.partial(
                utila.run,
                cmd=f'jam -i {inpath} -o {outpath} --remove={removepages}',
            ))
    # generate
    # ensure correct parent [dest]
    without_titlepage = [
        genex.config.todo(item, name=utila.file_name(item))
        for item in without_titlepage
    ]
    todolist = genex.todolist(without_titlepage, destination=dest, **kwargs)
    for index, job in enumerate(todolist):
        job = functools.partial(
            genex.run_job,
            job=job,
            number=(index, len(todolist) - 1),
        )
        todo.append(job)
    # avoid race condition that jam is not ready before starting extraction
    worker = utila.mins(len(files), worker)
    utila.fork(
        *todo,
        worker=worker,
        process=False,
    )

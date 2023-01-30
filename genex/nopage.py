# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

import resinf
import utila

import genex


def extract_removepages(
    resources,
    dest=None,
    removepages: str = '1:3',
    folder: str = 'notoc',
    worker: str = 8,
    **kwargs,
):
    assert worker <= len(resources), 'worker count too high, see jam and step after'  # yapf:disable
    dest, files = dest_and_files(resources, dest, folder)
    todo, without_titlepage = pdf_strip(
        files,
        removepages,
        dest=dest,
    )
    extract_pdf = generate(
        without_titlepage,
        dest,
        **kwargs,
    )
    todo.extend(extract_pdf)
    # avoid race condition that jam is not ready before starting extraction
    worker = utila.mins(len(files), worker)
    utila.fork(
        *todo,
        worker=worker,
        process=False,
    )


def dest_and_files(resources, dest, folder):
    # CLEAN UP THIS HACK Y PLACE
    dest = resinf.generated(folder=folder) if not dest else dest
    files = [
        item[0] if not isinstance(item, str) else item for item in resources
    ]
    return dest, files


def pdf_strip(files, removepages, dest):
    # prepare
    without_titlepage = [
        os.path.join(dest, f'{resinf.simple(item)}.pdf') for item in files
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
    # ensure correct parent [dest]
    without_titlepage = [
        resinf.todo(item, name=utila.file_name(item))
        for item in without_titlepage
    ]
    return todo, without_titlepage


def generate(
    without_titlepage,
    dest,
    **kwargs,
):
    # generate
    todolist = genex.todolist(without_titlepage, dest=dest, **kwargs)
    todo = []
    for index, job in enumerate(todolist):
        job = functools.partial(
            genex.run_job,
            job=job,
            number=(index, len(todolist) - 1),
        )
        todo.append(job)
    return todo

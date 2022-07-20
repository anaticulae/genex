# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Test-Data-Generator
===================

The purpose of this test-data-generator is to deliver easy to use test
data for following analysis steps.

Furthermore these examples shows how to use the different tools
together. We do not want to duplicate any generator code.
"""

import concurrent.futures
import os
import sys

import utila

import genex.automata
import genex.config
import genex.pages
import genex.utils


@utila.rename(rawmaker_cleanup='cleanup', destination='dest')
def extract(  # pylint:disable=R0914,R0913,W0613
    files: list,
    dest: str = None,
    pages: str = ':',
    worker: int = 12,
    rawmaker: str = genex.config.CONFIG,
    oneline: str = genex.config.ONELINE,
    *,
    cleanup: bool = False,
    optimize: bool = False,
    base: str = None,
    bibliography: bool = False,
    caption: bool = False,
    chapter: bool = False,
    codero: bool = False,
    color: bool = False,
    detector: bool = False,
    docref: bool = False,
    doctextstyle: bool = False,
    figureo: bool = False,
    formulero: bool = False,
    groupme: bool = False,
    headlines: bool = False,
    lists: bool = False,
    magic: bool = False,
    morefeatures: list = None,
    pagenumber: bool = False,
    pdfinfo: bool = True,
    reftable: bool = False,
    sections: bool = False,
    smarty: bool = False,
    spacestation: bool = False,
    tablero: bool = False,
    textflow: bool = False,
    weblink: bool = False,
    words: bool = False,
    full: bool = False,
):
    """Run rawmaker, groupme, sections and words for given `files` and write
    result to `dest`.

    Args:
        files(list): list of files to work on; list of pattern
                     (file, _pages_) or (file). If `_pages_` is given
                     use default var `pages`.
        dest(path): create folder for every file and save result
        pages(str): range of selected pages
        worker(int): number of threads to extract examples
        rawmaker(str): default config
        oneline(str): oneline config
        cleanup(str): run if True
        tablero(bool): run if True
        formulero(bool): run if True
        codero(bool): run if True
        color(bool): run if True
        pdfinfo(bool): run if True
        optimize(bool): run if True
        base(str): root to determine generated output names, see comment below
        ----------
        morefeatures(list): enable optional features
        bibliography(bool): run if True
        caption(bool): run if True
        chapter(bool): run if True
        detector(bool): run if True
        docref(bool): run if True
        doctextstyle(bool): run if True
        figureo(bool): run if True
        groupme(bool): run if True
        headlines(bool): run if True
        lists(bool): run if True
        magic(bool): run if True
        pagenumber(bool): run if True
        reftable(bool): run if True
        sections(bool): run if True
        smarty(bool): run if True
        spacestation(bool): run if True
        textflow(bool): run if True
        weblink(bool): run if True
        words(bool): run if True
        full(bool): overwrites every selection and runs all extraction steps
    Raises:
        Exception: if Exception occurs while extracting file
    """
    validate_files(files)
    # Ensure to handle single file generation or common resource subfolder
    # correctly. To determine the output path it is required to determine
    # the parent path of at least two files. If files provide only a
    # single file the common file pattern-determination is not possible.
    # Therefore we have to add the data root of all test files.
    dest = default_destination(dest)
    if utila.exists(dest):
        # disable write protection to enable regenaration
        utila.directory_unlock(dest, noerror=True)
    # TODO: REMOVE BASE LATER
    todo = todolist(
        files,
        dest,
        pages,
        bibliography=bibliography,
        caption=caption,
        chapter=chapter,
        cleanup=cleanup,
        codero=codero,
        color=color,
        detector=detector,
        docref=docref,
        doctextstyle=doctextstyle,
        figureo=figureo,
        formulero=formulero,
        groupme=groupme,
        headlines=headlines,
        lists=lists,
        magic=magic,
        oneline=oneline,
        optimize=optimize,
        pagenumber=pagenumber,
        pdfinfo=pdfinfo,
        rawmaker=rawmaker,
        reftable=reftable,
        sections=sections,
        smarty=smarty,
        spacestation=spacestation,
        tablero=tablero,
        textflow=textflow,
        weblink=weblink,
        words=words,
        full=full,
        morefeatures=morefeatures,
    )
    todomax = len(todo) - 1
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = [
            executor.submit(run_job, job, (index, todomax))
            for index, job in enumerate(todo)
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                comment = future.result()
                utila.info(comment)
            except Exception:
                utila.error(f'{future} failed.')
                raise
    # enable write protection to avoid changing generated data
    utila.directory_lock(dest, noerror=True)


def default_destination(dest: str) -> str:
    if dest is None:
        import power
        dest = power.generated()
    return dest


def validate_files(files: list):
    """Ensure that file is only defined once."""
    import power
    single = utila.Single()
    error = []
    for item in files:
        src = power.pdf(item)
        if not single.contains(src):
            continue
        error.append(src)
    if error:
        raise ValueError(f'duplicated resource: {error}')


@utila.rename(rawmaker_cleanup='cleanup', destination='dest')
def todolist(  # pylint:disable=R0914,R0913
    files: list,
    dest: str,
    pages: str = '0:10',
    rawmaker: str = genex.config.CONFIG,
    oneline: str = genex.config.ONELINE,
    tablero: bool = False,
    formulero: bool = False,
    codero: bool = False,
    pdfinfo: bool = True,
    color: bool = False,
    cleanup: bool = False,
    optimize: bool = False,
    *,
    bibliography: bool = False,
    caption: bool = False,
    chapter: bool = False,
    detector: bool = False,
    docref: bool = False,
    doctextstyle: bool = False,
    figureo: bool = False,
    groupme: bool = False,
    headlines: bool = False,
    lists: bool = False,
    magic: bool = False,
    pagenumber: bool = False,
    reftable: bool = False,
    sections: bool = False,
    smarty: bool = False,
    spacestation: bool = False,
    textflow: bool = False,
    weblink: bool = False,
    words: bool = False,
    full: bool = False,
    morefeatures: list = None,
):
    """Create todo list to extract resources.

        files: list of resources to extract. There are two list pattens:
               (file, pages) or (file).
        full: overwrites every selection and runs all extraction steps

    >>> todolist(['bachelor/bachelor090_PDF.pdf'], 'basedir', full=True)
    [(['pdfinfo...', 'rawmaker...-o=basedir/bachelor_bachelor090_PDF..., 'basedir/bachelor_bachelor090_PDF')]
    """
    if full:
        # enable every extraction step
        bibliography = True
        caption = True
        chapter = True
        cleanup = True
        codero = True
        color = True
        detector = True
        docref = True
        doctextstyle = True
        figureo = True
        formulero = True
        groupme = True
        headlines = True
        lists = True
        magic = True
        optimize = True
        pagenumber = True
        pdfinfo = True
        reftable = True
        sections = True
        smarty = True
        spacestation = True
        tablero = True
        textflow = True
        weblink = True
        words = True
    config = dict(
        bibliography=bibliography,
        caption=caption,
        chapter=chapter,
        cleanup=cleanup,
        color=color,
        detector=detector,
        docref=docref,
        doctextstyle=doctextstyle,
        figureo=figureo,
        groupme=groupme,
        headlines=headlines,
        lists=lists,
        magic=magic,
        optimize=optimize,
        pagenumber=pagenumber,
        reftable=reftable,
        sections=sections,
        smarty=smarty,
        spacestation=spacestation,
        textflow=textflow,
        weblink=weblink,
        words=words,
    )
    todo = generate(
        files,
        dest,
        pages=pages,
        config=config,
        rawmaker=rawmaker,
        oneline=oneline,
        pdfinfo=pdfinfo,
        tablero=tablero,
        formulero=formulero,
        codero=codero,
        morefeatures=morefeatures,
    )
    return todo


def run_job(job: tuple, number: tuple = None):  # pylint:disable=R0914
    steps, dest = job
    verbosity = -1 if utila.level_current() > utila.LEVEL_DEFAULT else 200
    # prepare run
    rawjob = utila.from_tuple(steps, separator=' && ')[0:verbosity]
    rawjob = utila.forward_slash(rawjob, keep_newline=False)
    # log job start
    number = '' if not number else f'[{number[0]}|{number[1]}] '
    utila.log(f'{number} {rawjob}')
    # create result folder
    os.makedirs(dest, exist_ok=True)
    # log job start to log folder
    logpath = os.path.join(dest, 'generated.log')
    if utila.exists(logpath):
        utila.log(f'already generated: {logpath}\nskip: {rawjob}\n')
        return
    logstep = lambda msg: utila.file_append(logpath, f'{msg}\n')
    utila.file_create(logpath, f'{utila.timedate()}\n')
    for index, step in enumerate(steps):
        if not isinstance(step, str):
            step, inpath, section = step
            pages = genex.pages.select_pages(inpath, section)
            if not pages:
                utila.debug(f'could not find section: {section}; skip: {step}')
                continue
            step += f' --pages={pages}'
        # log progress to log file
        index = str(index).zfill(2)
        forwarded = utila.forward_slash(step, keep_newline=False)
        logstep(f'::{index}>>{forwarded}')
        start = utila.now()
        completed = utila.run(
            step,
            expect=None,
        )
        diff = utila.now() - start
        if completed.stdout:
            logstep(completed.stdout)
        if completed.stderr:
            logstep(completed.stderr)
        logstep(f'runtime: {diff} sec\n')
        if completed.returncode:
            sys.exit(completed.returncode)
    # log final time
    logstep(utila.timedate())
    rawjob = genex.utils.shorten_path(rawjob)
    utila.log(f'completed: {rawjob}')


def generate(  # pylint:disable=R0914
    files: list,
    outpath: str,
    pages: str,
    config: dict,
    rawmaker: str,
    oneline: str,
    *,
    formulero: bool = True,
    pdfinfo: bool = True,
    tablero: bool = True,
    codero: bool = True,
    morefeatures: list = None,
) -> list:
    # TODO: MAY REMOVE LATER
    config = utila.dicts_united(
        config,
        dict(
            rawmaker=rawmaker,
            oneline=oneline,
            formulero=formulero,
            pdfinfo=pdfinfo,
            tablero=tablero,
            codero=codero,
        ),
    )
    files = genex.config.prepare_files(files, pages=pages)
    todo = []
    for resource in files:
        dest = utila.forward_slash(os.path.join(outpath, resource.name))
        jobconfig = utila.dicts_united(
            config,
            resource.config,
        )
        jobmaker = genex.automata.JobMaker(
            src=resource.resource,
            dest=dest,
            pages=resource.pages,
            config=jobconfig,
            more=morefeatures,
        )
        task = jobmaker.run()
        todo.append((task, dest))
    return todo

# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
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

import iamraw
import power
import utila
import utila.logger
import utilatest

import genex.config
import genex.pages


def extract(  # pylint:disable=R0914,R0913
    files: list,
    destination: str,
    pages: str = '0:10',
    worker: int = 12,
    rawmaker: str = genex.config.CONFIG,
    oneline: str = genex.config.ONELINE,
    *,
    rawmaker_cleanup: bool = True,
    figureo: bool = False,
    formulero: bool = True,
    pdfinfo: bool = True,
    tablero: bool = True,
    codero: bool = True,
    base: str = None,
    morefeatures: list = None,
    caption: bool = False,
    detector: bool = False,
    docref: bool = False,
    doctextstyle: bool = False,
    groupme: bool = False,
    magic: bool = False,
    sections: bool = False,
    smarty: bool = False,
    spacestation: bool = False,
    textflow: bool = False,
    words: bool = False,
    full: bool = False,
):
    """Run rawmaker, groupme, sections and words for given `files` and write
    result to `destination`.

    Args:
        files(list): list of files to work on; list of pattern
                     (file, _pages_) or (file). If `_pages_` is given
                     use default var `pages`.
        destination(path): create folder for every file and save result
        pages(str): range of selected pages
        worker(int): number of threads to extract examples
        rawmaker(str): default config
        oneline(str): oneline config
        rawmaker_cleanup(str): run if True
        tablero(bool): run if True
        formulero(bool): run if True
        codero(bool): run if True
        pdfinfo(bool): run if True
        base(str): root to determine generated output names, see comment below
        ----------
        morefeatures(list): enable optional features
        caption(bool): run if True
        detector(bool): run if True
        docref(bool): run if True
        doctextstyle(bool): run if True
        figureo(bool): run if True
        groupme(bool): run if True
        magic(bool): run if True
        sections(bool): run if True
        smarty(bool): run if True
        spacestation(bool): run if True
        textflow(bool): run if True
        words(bool): run if True
        full(bool): overwrites every selection and runs all extraction steps
    Raises:
        Exception: if Exception occurs while extracting file
    """
    # Ensure to handle single file generation or common resource subfolder
    # correctly. To determine the output path it is required to determine
    # the parent path of at least two files. If files provide only a
    # single file the common file pattern-determination is not possible.
    # Therefore we have to add the data root of all test files.
    base = [base] if base else [power.REPOSITORY]
    files = files + base
    todo = todolist(
        files,
        destination,
        pages,
        codero=codero,
        caption=caption,
        detector=detector,
        docref=docref,
        doctextstyle=doctextstyle,
        figureo=figureo,
        formulero=formulero,
        groupme=groupme,
        magic=magic,
        oneline=oneline,
        pdfinfo=pdfinfo,
        rawmaker=rawmaker,
        rawmaker_cleanup=rawmaker_cleanup,
        sections=sections,
        smarty=smarty,
        spacestation=spacestation,
        tablero=tablero,
        textflow=textflow,
        words=words,
        full=full,
        morefeatures=morefeatures,
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = [
            executor.submit(run_job, job, (index, len(todo) - 1))
            for index, job in enumerate(todo)
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                comment = future.result()
                utila.info(comment)
            except Exception:
                utila.info(f'{future} failed.')
                raise


def todolist(  # pylint:disable=R0914
    files: list,
    destination: str,
    pages: str = '0:10',
    rawmaker: str = genex.config.CONFIG,
    oneline: str = genex.config.ONELINE,
    tablero: bool = True,
    formulero: bool = True,
    codero: bool = True,
    pdfinfo: bool = True,
    rawmaker_cleanup: bool = True,
    *,
    caption: bool = False,
    detector: bool = False,
    docref: bool = False,
    doctextstyle: bool = False,
    figureo: bool = False,
    groupme: bool = False,
    magic: bool = False,
    sections: bool = False,
    smarty: bool = False,
    spacestation: bool = False,
    textflow: bool = False,
    words: bool = False,
    full: bool = False,
    morefeatures: list = None,
):
    """Create todo list to extract resources.

        files: list of resources to extract. There are two list pattens:
               (file, pages) or (file).
        full: overwrites every selection and runs all extraction steps
    """
    if full:
        # enable every extraction step
        caption = True
        codero = True
        detector = True
        docref = True
        doctextstyle = True
        figureo = True
        formulero = True
        groupme = True
        magic = True
        pdfinfo = True
        rawmaker_cleanup = True
        sections = True
        smarty = True
        spacestation = True
        tablero = True
        textflow = True
        words = True
    config = {
        'caption': caption,
        'detector': detector,
        'docref': docref,
        'doctextstyle': doctextstyle,
        'figureo': figureo,
        'groupme': groupme,
        'magic': magic,
        'sections': sections,
        'smarty': smarty,
        'spacestation': spacestation,
        'textflow': textflow,
        'words': words,
        'rawmaker_cleanup': rawmaker_cleanup,
    }
    todo = generate(
        files,
        destination,
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
    verbosity = -1 if utila.logger.LEVEL > utila.LEVEL_DEFAULT else 200
    # prepare run
    rawjob = utila.from_tuple(steps, separator=' && ')[0:verbosity]
    rawjob = utila.forward_slash(rawjob, newline=False)
    # log job start
    number = '' if not number else f'[{number[0]}|{number[1]}] '
    utila.log(f'{number} {rawjob}')
    # create result folder
    os.makedirs(dest, exist_ok=True)
    # log job start to log folder
    logpath = os.path.join(dest, 'generated.log')
    logstep = lambda msg: utila.file_append(logpath, f'{msg}\n')
    utila.file_create(logpath, f'{utila.timedate()}\n')
    for step in steps:
        if not isinstance(step, str):
            step, inpath, section = step
            pages = genex.pages.select_pages(inpath, section)
            step += f' --pages={pages}'
        # log progress to log file
        forwarded = utila.forward_slash(step, newline=False)
        logstep(forwarded)
        start = utila.now()
        completed = utila.run(step)
        diff = utila.now() - start
        logstep(completed.stdout)
        logstep(completed.stderr)
        logstep(f'runtime: {diff} sec')
        utila.assert_success(completed)
    # log final time
    logstep(f'{utila.timedate()}')
    utila.log(f'completed: {rawjob[0:100]}')


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
    todo = []
    singlepages = genex.pages.paged(files, default=pages)
    files = list(singlepages.keys())
    names = utilatest.simplify_testfile_names(files, sort=False)
    for inpath, output in zip(files, names):
        dest = os.path.join(outpath, output)
        nextjob = create_job(
            inpath,
            dest,
            pages=singlepages[inpath],
            config=config,
            rawmaker=rawmaker,
            oneline=oneline,
            tablero=tablero,
            formulero=formulero,
            pdfinfo=pdfinfo,
            codero=codero,
            morefeatures=morefeatures,
        )
        todo.append(nextjob)
    return todo


def create_job(  # pylint:disable=R1260,R0912
    src: str,
    dest: str,
    rawmaker: str,
    oneline: str,
    *,
    formulero: bool = True,
    pdfinfo: bool = True,
    tablero: bool = True,
    codero: bool = True,
    pages: tuple = None,
    config: dict = None,
    morefeatures: list = None,
) -> list:
    """Create job to run required steps for next processing unit.

    Args:
        src: pdf file for processing
        dest: output path to output folder
        rawmaker: default config
        oneline: default oneline config
        formulero: run formulero
        pdfinfo: run pdfinfo
        tablero: run tablero
        codero: run codero
        pages: shrink processing if given - if None process all pages
        config: select which processes to run
        morefeatures: add userbased features
    Returns:
        Created process todo description.
    """
    config = config if config else {}
    pages = f'--pages={pages}' if pages is not None else ''
    # ensure that testdir.tmpdir is converted to str before using forward_slash
    src, dest = str(src), str(dest)
    src = utila.forward_slash(src, newline=False)
    dest = utila.forward_slash(dest, newline=False)
    task = [
        f'rawmaker -j=auto -i={src} -o={dest} {rawmaker} {pages}',
    ]
    if oneline:
        # skip with oneline = None
        task.append(f'rawmaker -j=auto -i={src} -o={dest} {oneline} {pages}')
    if pdfinfo:
        task.append(f'pdfinfo -i={src} -o={dest} --format=yaml')
    if formulero:
        task.append(f'formulero -i={src} -o={dest} {pages} -j2')
    if config.get('spacestation', False):
        task.append(f'spacestation -i={src} -o={dest} {pages}')
    groupme = config.get('groupme', False)
    if groupme:
        if isinstance(groupme, str):
            # use specialized groupme config
            task.append(f'groupme -i={dest} -o={dest} {groupme}')
        else:
            # run all, disable --toc
            task.append(f'groupme --toc! --abbreviation! -j=auto -i={dest} '
                        f'-o={dest}')
            # toc only
            task.append(f'groupme --toc --pages=0:10 -i={dest} -o={dest}')
    if tablero:
        task.append(f'groupme -i={dest} -o={dest} --content')
        task.append(f'tablero -i={dest} --table={src} -o={dest} {pages} '
                    '-j=auto')
        task.append(f'groupme -i={dest} -o={dest} --area')
    if codero:
        task.append(f'codero -i={dest} -o={dest} -j1')
    if config.get('figureo', False):
        task.append(f'figureo -i={src} -i={dest} -o={dest} {pages}')
    if config.get('rawmaker_cleanup', False):
        task.append(f'rawmaker_cleanup -i={dest} -o={dest} --backup {pages}')
        if oneline:
            task.append(f'rawmaker_cleanup -i={dest} -o={dest} '
                        f'--prefix=oneline --backup {pages}')
    if config.get('sections', False):
        task.append(f'sections -i={dest} --pdf={src} -o={dest} {pages}')
    task.extend(select_features(config, dest, morefeatures))
    return task, dest


FEATURES = [  # Hint: Pay attention to the order
    ('groupme --abbreviation', iamraw.sections.AbbreviationTable),
    'magic',
    'words',
    'docref',
    ('detector --bibliography ', iamraw.sections.Bibliography),
    ('detector --titlepage ', iamraw.sections.TitlePage),
    'detector --formula ',
    'textflow --wordspace!',
    'doctextstyle',
    'caption',
    'magic',
    'textflow --wordspace',
    'smarty',
]


def select_features(config: dict, dest: str, morefeatures: list) -> list:
    # create a copy to avoid side effects, that disabling groupme does not
    # interfere with further steps.
    config = dict(config)
    features = FEATURES[:]
    if morefeatures:
        features.extend(morefeatures)
        # enable all optional features
        for item in morefeatures:
            if not isinstance(item, str):
                item, _ = item
            config[item] = True
    if not config.get('sections', False):
        # disable groupme --abbreviations cause sections_result is
        # required.
        config['groupme'] = False
    task = []
    for feature in features:
        if not isinstance(feature, str):
            feature, section = feature
        else:
            section = None
        if not config.get(feature.split()[0], False):
            continue
        if section:
            task.append((
                f'{feature} -j=auto -i={dest} -o={dest}',
                dest,
                section,
            ))
        else:
            task.append(f'{feature} -j=auto -i={dest} -o={dest}')
    return task

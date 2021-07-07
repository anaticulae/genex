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

The purpose of this test-data-generator is to deliver easy use test data
for following analysis steps. Furthermore these examples shows how to
use the different tools together. We do not want to duplicate any
generator code.
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
import genex.utils


def extract(  # pylint:disable=R0914
    files: list,
    destination: str,
    pages: str = '0:10',
    worker: int = 12,
    rawmaker: str = genex.config.CONFIG,
    oneline: str = genex.config.ONELINE,
    base: str = None,
    *,
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
        base(str): root to determine generated output names, see comment below
        ----------
        morefeatures(list): enable optional features
        caption(bool): run if True
        detector(bool): run if True
        docref(bool): run if True
        doctextstyle(bool): run if True
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
        caption=caption,
        detector=detector,
        docref=docref,
        doctextstyle=doctextstyle,
        groupme=groupme,
        magic=magic,
        oneline=oneline,
        rawmaker=rawmaker,
        sections=sections,
        smarty=smarty,
        textflow=textflow,
        words=words,
        spacestation=spacestation,
        full=full,
        morefeatures=morefeatures,
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=worker) as executor:
        futures = [executor.submit(run_job, job) for job in todo]
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
    *,
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
        detector = True
        docref = True
        doctextstyle = True
        groupme = True
        magic = True
        sections = True
        smarty = True
        textflow = True
        words = True
        spacestation = True

    config = {
        'caption': caption,
        'detector': detector,
        'docref': docref,
        'doctextstyle': doctextstyle,
        'groupme': groupme,
        'magic': magic,
        'sections': sections,
        'smarty': smarty,
        'spacestation': spacestation,
        'textflow': textflow,
        'words': words,
    }
    todo = generate(
        files,
        destination,
        pages=pages,
        config=config,
        rawmaker=rawmaker,
        oneline=oneline,
        morefeatures=morefeatures,
    )
    return todo


def run_job(job: tuple):
    steps, destination = job
    verbosity = -1 if utila.logger.LEVEL > utila.LEVEL_DEFAULT else 200
    rawjob = ' && '.join([str(item) for item in steps])[0:verbosity]
    rawjob = utila.forward_slash(rawjob)
    utila.log(f'start: {rawjob}')
    os.makedirs(destination, exist_ok=True)
    logpath = os.path.join(destination, 'generated.log')
    utila.file_create(logpath, utila.timedate())
    for step in steps:
        if not isinstance(step, str):
            step, inpath, section = step
            pages = genex.pages.select_pages(inpath, section)
            step += f' --pages={pages}'
        completed = utila.run(step)
        # log progress to log file
        utila.file_append(logpath, step)
        utila.file_append(logpath, completed.stderr)
        utila.file_append(logpath, completed.stdout)
        utila.assert_success(completed)
    utila.log(f'completed: {rawjob[0:100]}')


def generate(
    files: list,
    outpath: str,
    pages: str,
    config: dict,
    rawmaker: str,
    oneline: str,
    morefeatures: list = None,
) -> list:
    todo = []
    singlepages = genex.utils.paged(files, default=pages)
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
            morefeatures=morefeatures,
        )
        todo.append(nextjob)
    return todo


def create_job(
    src: str,
    dest: str,
    rawmaker: str,
    oneline: str,
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
        pages: shrink processing if given - if None process all pages
        config: select which processes to run
        morefeatures: add userbased features
    Returns:
        Created process todo description.
    """
    config = config if config else {}
    pages = f'--pages={pages}' if pages is not None else ''
    task = [
        f'rawmaker -j=auto -i={src} -o={dest} {rawmaker} {pages}',
        f'rawmaker -j=auto -i={src} -o={dest} {oneline} {pages}',
        f'linero -i={dest} -o={dest}',
        f'pdfinfo -i={src} -o={dest} --format=yaml',
    ]
    if config.get('spacestation', False):
        task.append(f'spacestation -i={src} -o={dest} {pages}')
    groupme = config.get('groupme', False)
    if groupme:
        if isinstance(groupme, str):
            # use specialized groupme config
            task.append(f'groupme -i={dest} -o={dest} {groupme}')
        else:
            # run all, disable --toc
            task.append(f'groupme --toc! --abbreviation! -j=auto -i={dest} -o={dest}') # yapf:disable
            # toc only
            task.append(f'groupme --toc --pages=0:10 -i={dest} -o={dest}')
    task.extend(select_features(config, dest, morefeatures))
    return task, dest


FEATURES = [  # Hint: Pay attention to the order
    'sections',
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

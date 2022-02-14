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

import iamraw
import utila
import utila.logger

import genex.config
import genex.pages
import genex.utils


def extract(  # pylint:disable=R0914,R0913,W0613
    files: list,
    destination: str,
    pages: str = '0:10',
    worker: int = 12,
    rawmaker: str = genex.config.CONFIG,
    oneline: str = genex.config.ONELINE,
    *,
    rawmaker_cleanup: bool = False,
    optimize: bool = False,
    figureo: bool = False,
    formulero: bool = False,
    pdfinfo: bool = True,
    tablero: bool = False,
    codero: bool = False,
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
        optimize(bool): run if True
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
    # TODO: REMOVE BASE LATER
    todo = todolist(
        files,
        destination,
        pages,
        caption=caption,
        codero=codero,
        detector=detector,
        docref=docref,
        doctextstyle=doctextstyle,
        figureo=figureo,
        formulero=formulero,
        groupme=groupme,
        magic=magic,
        oneline=oneline,
        optimize=optimize,
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


def todolist(  # pylint:disable=R0914,R0913
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
    optimize: bool = False,
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
        optimize = True
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
        'optimize': optimize,
        'rawmaker_cleanup': rawmaker_cleanup,
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
    rawjob = utila.forward_slash(rawjob, keep_newline=False)
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
            if not pages:
                utila.debug(f'skip: {step}')
                continue
            step += f' --pages={pages}'
        # log progress to log file
        forwarded = utila.forward_slash(step, keep_newline=False)
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
    todo = []
    files = genex.config.prepare_files(files, pages=pages)
    for resource in files:
        dest = os.path.join(outpath, resource.name)
        nextjob = create_job(
            resource.resource,
            dest,
            pages=resource.pages,
            config=config,
            rawmaker=rawmaker,
            oneline=oneline,
            tablero=tablero,
            formulero=formulero,
            pdfinfo=pdfinfo,
            codero=codero,
            morefeatures=morefeatures,
            overwrite=resource.config,
        )
        todo.append(nextjob)
    return todo


@utila.defaults_overwrite
def create_job(  # pylint:disable=R1260,R0912,R0914
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
    # pylint:disable=W0613
    overwrite: dict = None,
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
        overwrite: overwrite config
    Returns:
        Created process todo description.
    """
    src, dest, pages, config, dd, sd, sdp, ddp, sddp = prepare(  # pylint:disable=C0103
        src, dest, pages, config)
    groupme = config.get('groupme', False)
    groupme_complex = groupme and not isinstance(groupme, str)
    cleanup = config.get('rawmaker_cleanup', False)
    # yapf:disable
    task = [
        f'rawmaker -j=auto {sdp} {rawmaker}',
        (f'rawmaker -j=auto {sdp} {oneline}', oneline),
        (f'pdfinfo {sd} --format=yaml', pdfinfo),
        (f'formulero {sdp} -j2', formulero),
        (f'spacestation {sdp}', config.get('spacestation', False)),
        # groupme-simple
        # use specialized groupme config
        (f'groupme {dd} {groupme}', groupme and not groupme_complex),
        # groupme-complex
        # run all, disable --toc
        (f'groupme --toc! --abbreviation! -j=auto {dd}', groupme_complex),
        # toc only
        (f'groupme --toc --pages=0:10 {dd}', groupme_complex),
        # tablero
        (f'groupme {dd} --pagenumbers --footer --content', tablero and not groupme),
        (f'tablero --table={src} {ddp} -j=auto', tablero),
        (f'groupme {dd} --area', tablero),
        # codero
        (f'codero {dd} -j1', codero),
        # figureo
        # separate steps are required, cause standard produces figure
        # files which are required for cleanup step. In the current state
        # utila determines inputs only at startup time. Therefore figureo
        # wont know than theses later generated files exists.
        # TODO: REMOVE AFTER UPGRADING INPUTS AFTER EVERY STEP
        (f'figureo --standard {sddp}', config.get('figureo', False)),
        (f'figureo --cleanup {sddp}', config.get('figureo', False)),
        # rawmaker_cleanup
        (f'rawmaker_cleanup {ddp}', cleanup),
        (f'rawmaker_cleanup --prefix=oneline {ddp}', cleanup and oneline),
        # sections
        (f'sections --pdf={src} {ddp}', config.get('sections', False)),
    ]
    # remove disabled tasks
    task = [item for item in task if isinstance(item, str) or item[1]]
    task = [item if isinstance(item, str) else item[0] for item in task]
    # yapf:enable
    task.extend(select_features(config, dest, morefeatures))
    return task, dest


FEATURES = [  # Hint: Pay attention to the order
    ('groupme --abbreviation', iamraw.sections.AbbreviationTable),
    'caption',
    'magic',
    'words',
    'docref',
    ('detector --bibliography ', iamraw.sections.Bibliography),
    ('detector --titlepage ', iamraw.sections.TitlePage),
    'detector --formula ',
    'textflow --wordspace!',
    'doctextstyle',
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
    if config.get('optimize', False):
        task.append(f'findings --optimize -i={dest} -o={dest}')
    return task


def prepare(src, dest, pages, config) -> tuple:
    # ensure that testdir.tmpdir is converted to str before using forward_slash
    src, dest = str(src), str(dest)
    src = utila.forward_slash(src, keep_newline=False)
    dest = utila.forward_slash(dest, keep_newline=False)
    pages = f'--pages={pages}' if pages is not None else ''
    config = config if config else {}
    dd = f'-i={dest} -o={dest}'  # pylint:disable=C0103
    sd = f'-i={src} -o={dest}'  # pylint:disable=C0103
    sdp = f'-i={src} -o={dest} {pages}'
    ddp = f'-i={dest} -o={dest} {pages}'
    sddp = f'-i={src} -i={dest} -o={dest} {pages}'
    return src, dest, pages, config, dd, sd, sdp, ddp, sddp

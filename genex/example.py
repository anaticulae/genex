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
    tablero: bool = False,
    formulero: bool = False,
    codero: bool = False,
    pdfinfo: bool = True,
    rawmaker_cleanup: bool = False,
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

    >>> todolist(['bachelor/bachelor090_PDF.pdf'], 'basedir', full=True)
    [(['rawmaker...-o=basedir/bachelor_bachelor090_PDF..., 'basedir/bachelor_bachelor090_PDF')]
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
    for index, step in enumerate(steps):
        if not isinstance(step, str):
            step, inpath, section = step
            pages = genex.pages.select_pages(inpath, section)
            if not pages:
                utila.error(f'could not find section: {section}; skip: {step}')
                continue
            step += f' --pages={pages}'
        # log progress to log file
        index = str(index).zfill(2)
        forwarded = utila.forward_slash(step, keep_newline=False)
        logstep(f'::{index}>>{forwarded}')
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
        jobmaker = JobMaker(
            src=resource.resource,
            dest=dest,
            pages=resource.pages,
            config=jobconfig,
            more=morefeatures,
        )
        task = jobmaker.run()
        todo.append((task, dest))
    return todo


class JobMaker:  # pylint:disable=R0904
    """JobMaker
    ========

    Convert job config to executable job order.

    HINT: DO NOT CHANGE METHOD ORDER OF ADD_.

    Example
    ~~~~~~~

    >>> job = JobMaker('src', 'dest', '0:10', config=dict(rawmaker='config'))
    >>> job.run()
    ['rawmaker -j=auto -i=src -o=dest --pages=0:10 config']
    """

    def __init__(self, src, dest, pages: str, config: dict, more: list = None):
        src, dest = str(src), str(dest)
        self.src = utila.forward_slash(src, keep_newline=False)
        self.dest = utila.forward_slash(dest, keep_newline=False)
        self.pages = f'--pages={pages}' if pages is not None else ''
        self.config = dict(config) if config else {}
        self.more = more
        self.extend_config()

    def run(self) -> list:
        result = []
        methods = utila.methods(self, starts='add_')
        assert methods[-1] == self.add_optimize, 'optimize last'  # pylint:disable=W0143
        for method in methods:
            task = method()
            if not task:
                continue
            if isinstance(task, str):
                result.append(task)
            else:
                result.extend(task)
        result = self.expand_sections(result)
        return result

    def expand_sections(self, todo):
        result = []
        for feature in todo:
            if isinstance(feature, str):
                result.append(feature)
                continue
            feature, section = feature
            result.append((feature, self.dest, section))
        return result

    def extend_config(self):
        if not self.more:
            return
        # enable all optional features
        for item in self.more:
            if not isinstance(item, str):
                item, _ = item
            self.config[item] = True

    ############################################################################
    # DEFINE AUTOMATA
    ############################################################################

    def add_basic(self):
        result = [f'rawmaker -j=auto {self.sdp} {self.rawmaker}']
        if self.oneline:
            result += [f'rawmaker -j=auto {self.sdp} {self.oneline}']
        if self.pdfinfo:
            result += [f'pdfinfo {self.sd} --format=yaml']
        if self.formulero:
            result += [f'formulero {self.sdp} -j2']
        if self.spacestation:
            result += [f'spacestation {self.sdp}']
        return result

    def add_groupme(self):
        result = []
        if isinstance(self.groupme, str):
            # use specialized groupme config
            result += [f'groupme {self.dd} {self.groupme}']
        elif self.groupme:
            # run all, disable --toc
            result += [
                self.auto(
                    'groupme --toc! --abbreviation! --figuretable! --tabletable!'
                )
            ]
        return result

    def add_tablero(self):
        if not self.tablero:
            return []
        result = []
        if not self.groupme:
            result += [f'groupme {self.dd} --pagenumbers --footer --content']
        result += [
            f'tablero --table={self.src} {self.ddp} -j=auto',
            f'groupme {self.dd} --area',
        ]
        return result

    def add_codero(self):
        return f'codero {self.dd} -j1' if self.codero else None

    def add_figureo(self):
        if not self.figureo:
            return []
        # separate steps are required, cause standard produces figure
        # files which are required for cleanup step. In the current state
        # utila determines inputs only at startup time. Therefore figureo
        # wont know than theses later generated files exists.
        # TODO: REMOVE AFTER UPGRADING INPUTS AFTER EVERY STEP
        return [
            f'figureo --standard {self.sddp}',
            f'figureo --cleanup {self.sddp}',
        ]

    def add_rawmaker_cleanup(self):
        if not self.cleanup:
            return []
        result = [
            f'rawmaker_cleanup {self.ddp}',
        ]
        if self.oneline:
            result += [f'rawmaker_cleanup --prefix=oneline {self.ddp}']
        return result

    def add_sections(self):
        if not self.sections:
            return None
        return f'sections --pdf={self.src} {self.ddp}'

    def add_groupme_selected(self):
        if not self.sections or not self.groupme:
            return []
        return [
            (self.auto('groupme --toc'), iamraw.TableOfContent),
            (self.auto('groupme --abbreviation'), iamraw.AbbreviationTable),
            (self.auto('groupme --tabletable'), iamraw.TableTable),
            (self.auto('groupme --figuretable'), iamraw.FigureTable),
        ]

    def add_caption(self):
        # TODO: USE DECORATOR
        return self.auto('caption') if self.caption else None

    def add_magic(self):
        return self.auto('magic') if self.magic else None

    def add_words(self):
        if not self.words:
            return None
        if not self.sections:
            return self.auto('words')
        return [
            self.auto('words --headlines'),
            (self.auto('words --headlines!'), iamraw.MainPart),
        ]

    def add_docref(self):
        return self.auto('docref') if self.docref else None

    def add_detector(self):
        if not self.detector:
            return None
        if not self.sections:
            return self.auto('detector --formula')
        return [
            (self.auto('detector --bibliography'), iamraw.Bibliography),
            (self.auto('detector --titlepage'), iamraw.TitlePageSection),
            self.auto('detector --formula'),
        ]

    def add_textflow_no_wordspace(self):
        return self.auto('textflow --wordspace!') if self.textflow else None

    def add_doctextstyle(self):
        return self.auto('doctextstyle') if self.doctextstyle else None

    def add_magic_again(self):
        return self.auto('magic') if self.magic else None

    def add_textflow_wordspace(self):
        return self.auto('textflow --wordspace') if self.textflow else None

    def add_smarty(self):
        return self.auto('smarty') if self.smarty else None

    def add_optimize(self):
        # last method
        if not self.optimize:
            return None
        return f'findings --optimize -i={self.dest} -o={self.dest}'

    ############################################################################
    # END AUTOMATA
    ############################################################################

    @property
    def dd(self):  # pylint:disable=C0103
        return f'-i={self.dest} -o={self.dest}'

    @property
    def sd(self):  # pylint:disable=C0103
        return f'-i={self.src} -o={self.dest}'

    @property
    def sdp(self):
        return f'{self.sd} {self.pages}'

    @property
    def ddp(self):
        return f'{self.dd} {self.pages}'

    @property
    def sddp(self):
        return f'-i={self.src} -i={self.dest} -o={self.dest} {self.pages}'

    def auto(self, cmd):
        return f'{cmd} -j=auto {self.dd}'

    def __getattr__(self, name):
        return self.config.get(name, None)

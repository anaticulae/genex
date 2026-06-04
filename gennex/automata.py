# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import utilo


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
    >>> job = JobMaker('src', 'dest', '0:10', config=dict(words=True, sections=True))
    >>> job.run()
    [...('words --headlines! -j=auto -i=dest -o=dest', 'dest', (<class 'iamraw.sections.MainPart'>, True))]
    >>> job = JobMaker('src', 'dest', '0:10', config=dict(lists=True))
    >>> job.run()
    [...('lists -j=auto -i=dest -o=dest', 'dest', (<class 'iamraw.sections.MainPart'>, <class 'iamraw.sections.Appendix'>))]
    """

    def __init__(self, src, dest, pages: str, config: dict, more: list = None):
        src, dest = str(src), str(dest)
        self.src = utilo.forward_slash(src, keep_newline=False)
        self.dest = utilo.forward_slash(dest, keep_newline=False)
        self.pages = f'--pages={pages}' if pages is not None else ''
        self.config = dict(config) if config else {}
        self.more = more
        self.extend_config()

    def run(self) -> list:
        result = []
        methods = utilo.methods(self, starts='add_')
        assert methods[-1] == self.add_optimize, f'optimize last: {methods}'  # pylint:disable=W0143
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
        result = []
        if self.pdflog:
            result += [f'pdflog {self.sd} --format=yaml']
        if True:  # pylint:disable=using-constant-test
            # without rawmaker this makes no sense
            result += [f'rawmaker -j=auto {self.sdp} {self.rawmaker}']
        if self.oneline:
            result += [f'rawmaker -j=auto {self.sdp} {self.oneline}']
        if self.mundare:
            # save rawmaker result to ease debugging
            result += [f'mundare --backup {self.ddp}']
        if self.formulero:
            result += [f'formulero {self.sdp} -j2']
        if self.spacestation:
            result += [f'spacestation {self.sdp}']
        if self.color:
            result += [f'colors {self.sdp}']
        return result

    def add_pagenumber(self):
        if not self.pagenumber:
            return None
        result = [f'pagenumber {self.dd}']
        if self.mundare:
            # hide pagenumber to improve further processing
            result += [f'mundare --mundare {self.ddp} --select pagenumber']
        return result

    def add_footnote(self):
        if not self.footnote:
            return None
        result = [f'footnote {self.dd} -j2']
        if self.mundare:
            # hide pagenumber to improve further processing
            result += [f'mundare --mundare {self.ddp} --select footnote']
        return result

    def add_headnote(self):
        if not self.headnote:
            return None
        result = [f'headnote {self.dd} -j2']
        if self.mundare:
            # hide pagenumber to improve further processing
            result += [f'mundare --mundare {self.ddp} --select headnote']
        return result

    def add_groupme(self):
        result = []
        if isinstance(self.groupme, str):
            # use specialized groupme config
            result += [f'groupme {self.dd} {self.groupme}']
        elif self.groupme:
            result += [self.auto('groupme')]
        return result

    def add_tablero(self):
        if not self.tablero:
            return []
        result = []
        if not self.footnote:
            result += [f'footnote {self.dd} -j2']
        if not self.groupme:
            result += [f'groupme {self.dd} --content']
        if not self.pagenumber:
            result += [f'pagenumber {self.dd}']
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
        # files which are required for mundare step. In the current state
        # utilo determines inputs only at startup time. Therefore figureo
        # want know that those later generated files exists.
        # TODO: REMOVE AFTER UPGRADING INPUTS AFTER EVERY STEP
        return [
            f'figureo --standard {self.sddp}',
            f'figureo --mundare {self.sddp}',
        ]

    def add_caption(self):
        # TODO: USE DECORATOR
        return self.auto('caption') if self.caption else None

    def add_mundare(self):
        if not self.mundare:
            return []
        # skip backup if pagenumber is generated, this step is already done
        nobackup = '--backup!' if self.pagenumber else ''
        result = [
            f'mundare {self.ddp} {nobackup}',
        ]
        if self.oneline:
            result += [f'mundare --prefix=oneline {self.ddp}']
        if self.footnote:
            # run groupme again
            result += [f'footnote {self.dd} -j2']
        if self.pagenumber:
            # run pagenumber again TODO: GOOD IDEA?
            result += [f'pagenumber {self.dd}']
        return result

    def add_sections_ref(self):
        if not self.sections_ref:
            return None
        result = [
            f'sections_ref {self.dd} -j=auto',
        ]
        return result

    def add_sections(self):
        if not self.sections:
            return None
        result = []
        if not self.sections_ref:
            result += [
                f'sections_ref {self.dd} -j=auto',
            ]
        result += [
            f'sections --pdf={self.src} {self.ddp} -j=auto',
        ]
        return result

    def add_reftable_selected(self):
        if not self.sections or not self.reftable:
            return []
        return [
            (self.auto('reftable --toc'), iamraw.TableOfContent),
            (self.auto('reftable --abbrev'), iamraw.AbbreviationTable),
            (self.auto('reftable --table'), iamraw.TableTable),
            (self.auto('reftable --figure'), iamraw.FigureTable),
        ]

    def add_magic(self):
        return self.auto('magic') if self.magic else None

    def add_headlines(self):
        return self.auto('headlines') if self.headlines else None

    def add_lists(self):
        if not self.lists:
            return None
        # do not run lists on table of content or title page etc.
        result = [
            (self.auto('lists'), (iamraw.MainPart, iamraw.Appendix)),
        ]
        return result

    def add_words(self):
        if not self.words:
            return None
        if not self.sections:
            return self.auto('words --headlines!')
        return [
            (self.auto('words --headlines!'), (iamraw.MainPart, True)),
        ]

    def add_docref(self):
        return self.auto('docref') if self.docref else None

    def add_bibliography(self):
        if not self.bibliography:
            return None
        if not self.sections:
            return None
        return [(self.auto('bibliography'), iamraw.Bibliography)]

    def add_detector(self):
        if not self.detector:
            return None
        if not self.sections:
            return self.auto('detector --formula')
        return [
            (self.auto('detector --titlepage'), iamraw.TitlePageSection),
            (self.auto('detector --index'), iamraw.Index),
            self.auto('detector --formula'),
        ]

    def add_weblink(self):
        return self.auto('weblink') if self.weblink else None

    def add_textflow_no_wordspace(self):
        return self.auto('textflow --wordspace!') if self.textflow else None

    def add_doctextstyle(self):
        return self.auto('doctextstyle') if self.doctextstyle else None

    def add_magic_again(self):
        return self.auto('magic') if self.magic else None

    def add_textflow_wordspace(self):
        return self.auto('textflow --wordspace') if self.textflow else None

    def add_chapter(self):
        return self.auto('chapter') if self.chapter else None

    def add_smarty(self):
        return self.auto('smarty') if self.smarty else None

    def add_more(self):
        if not self.more:
            return None
        result = []
        for item in self.more:
            if not isinstance(item, str):
                # TODO: VERIFY SECOND
                item, _ = item
            result.append(self.auto(item))
        return result

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

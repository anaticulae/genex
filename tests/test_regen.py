# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import utilo
import utilotest

import genex.cli.regen


def run_genex_regen(cmd: str, mp, generated=None, expect=True) -> int:
    completed = utilotest.run_cov(
        cmd,
        genex.cli.regen.PROCESS,
        functools.partial(genex.cli.regen.main, generated=generated),
        expect=expect,
        mp=mp,
    )
    return completed


@utilotest.longrun
def test_cli_regen(td, mp):
    files = [
        hoverpower.BACHELOR090_PDF,
    ]
    genex.extract(
        files,
        dest=td.tmpdir,
        oneline=None,
        footnote=True,
        groupme=True,
        headnote=True,
        pagenumber=True,
        base=hoverpower.REPO,
        pages='0:5',
    )
    generated = td.tmpdir.join('bachelor_bachelor090')
    utilo.exists_assert(generated)
    with utilo.capture_stdout() as stdout:
        # start after third step
        run_genex_regen(cmd='3', mp=mp, generated=td.tmpdir)
    assert 'Steps: 3 Start: 3' in stdout()


def test_cli_regen_error(td, mp, capsys):
    run_genex_regen(cmd='0', mp=mp, generated=td.tmpdir, expect=False)
    stderr = utilotest.stderr(capsys)
    assert 'nothing todo:' in stderr

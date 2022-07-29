# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import power
import utila
import utilatest

import genex.cli.regen


def run_genex_regen(cmd: str, mp, generated=None) -> int:
    completed = utilatest.run_cov(
        cmd,
        genex.cli.regen.PROCESS,
        functools.partial(genex.cli.regen.main, generated=generated),
        expect=True,
        mp=mp,
    )
    return completed


@utilatest.longrun
def test_cli_regen(td, mp):
    files = [
        power.BACHELOR090_PDF,
    ]
    genex.extract(
        files,
        dest=td.tmpdir,
        oneline=None,
        pagenumber=True,
        groupme=True,
        base=power.REPOSITORY,
        pages='0:5',
    )
    generated = td.tmpdir.join('bachelor_bachelor090')
    utila.exists_assert(generated)
    with utila.capture_stdout() as stdout:
        # start after third step
        run_genex_regen(cmd='3', mp=mp, generated=td.tmpdir)
    assert 'Steps: 1 Start: 3' in stdout()

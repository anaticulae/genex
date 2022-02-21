# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import utila
import utilatest

import genex


@utilatest.longrun
def test_select_titlepage(testdir):
    files = [
        power.BACHELOR090_PDF,
    ]
    genex.extract(
        files,
        destination=testdir.tmpdir,
        groupme=True,
        sections=True,
        detector=False,
        base=power.REPOSITORY,
        pages='0:10',
    )
    generated = testdir.tmpdir.join('bachelor_bachelor090')
    utila.exists_assert(generated)
    selected = genex.select_pages(generated, select=iamraw.TitlePageSection)
    assert selected == '1'

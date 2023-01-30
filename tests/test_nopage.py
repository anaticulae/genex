# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utilatest

import genex


@utilatest.longrun
def test_nopage_extract(td):
    generated = td.tmpdir.join('generated')
    pdfs = [
        power.DOCU009_PDF,
        power.HOME018_PDF,
    ]
    genex.extract_removepages(
        resources=pdfs,
        dest=generated,
        pagenumber=True,
        headnote=True,
        footnote=True,
        groupme=True,
        worker=len(pdfs),
    )
    assert os.path.exists(generated), str(generated)


@utilatest.nightly
def test_nopage_full(td):
    generated = td.tmpdir.join('generated')
    pdfs = [
        power.DOCU009_PDF,
        power.DOCU007_PDF,
    ]
    genex.extract_removepages(
        resources=pdfs,
        dest=generated,
        full=True,
        worker=len(pdfs),
    )
    assert os.path.exists(generated), str(generated)

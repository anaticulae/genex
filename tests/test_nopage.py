# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
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
        groupme=True,
    )
    assert os.path.exists(generated), str(generated)

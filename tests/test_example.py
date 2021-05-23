# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utilatest

import genex


def test_example_common_root():
    pdfs = [
        power.DOCU09_PDF,
        power.BACHELOR111_PDF,
    ]
    expected = {
        'docu_docu009',
        'bachelor_bachelor111',
    }
    root = utilatest.simplify_testfile_names(pdfs)
    # the expected order is not important
    root = set(root)  # pylint:disable=R0204
    assert root == expected


@utilatest.longrun
def test_example_extract(testdir):
    generated = os.path.join(testdir.tmpdir, 'generated')
    pdfs = [
        power.DOCU09_PDF,
        power.BACHELOR111_PDF,
    ]
    genex.extract(
        pdfs,
        generated,
        pages='0:5',
        groupme=True,
        doctextstyle=True,
        sections=True,
        detector=True,
        spacestation=True,
    )
    assert os.path.exists(generated), str(generated)


def test_example_disable_abbreviation_step(testdir):
    """Disable groupme --abbreviation if sections is disabled cause
    groupme --abbreviations requires section_result."""
    generated = os.path.join(testdir.tmpdir, 'generated')
    pdfs = [
        power.DOCU09_PDF,
    ]
    genex.extract(
        pdfs,
        generated,
        pages='0:5',
        groupme=True,
        sections=False,
        base=power.REPOSITORY,
    )
    assert os.path.exists(generated), str(generated)


def test_example_order():
    todo, _ = genex.create_job(
        'source',
        'dest',
        'rawmaker_normal',
        'rawmaker_oneline',
        config=dict(
            caption=True,
            magic=True,
        ),
    )
    todo = ' && '.join(todo)  # pylint:disable=R0204
    # ensure to run caption before magic
    assert todo.find('caption') < todo.find('magic')

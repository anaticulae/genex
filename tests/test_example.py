# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
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
        'bachelor_page_111_images_toc',
        'docu_porting_extension_modules',
    }
    root = utilatest.simplify_testfile_names(pdfs)
    # the expected order is not important
    root = set(root)  # pylint:disable=R0204
    assert root == expected


def test_example_extract(testdir):
    root = str(testdir)
    generated = os.path.join(root, 'generated')
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
    )
    assert os.path.exists(generated), str(generated)


def test_example_order():
    todo = genex.create_job(
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

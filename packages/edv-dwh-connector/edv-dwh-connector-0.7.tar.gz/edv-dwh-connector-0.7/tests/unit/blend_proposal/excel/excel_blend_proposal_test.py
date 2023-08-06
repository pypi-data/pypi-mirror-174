"""
Test case for ExcelBlendProposal.
.. since: 0.1
"""

# -*- coding: utf-8 -*-
# Copyright (c) 2022 Endeavour Mining
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to read
# the Software only. Permissions is hereby NOT GRANTED to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import date
import openpyxl  # type: ignore
from hamcrest import assert_that, equal_to
from tests.unit.blend_proposal.excel.fake_start_cell import FakeStartCell
from edv_dwh_connector.blend_proposal.excel.excel_blend_proposal \
    import ExcelBlendProposal


BLEND_FILE_NAME = "3.Daily_Blend_Template_process_October.xlsx"


def test_gets_a_blend(resource_path_root) -> None:
    """
    Tests that it gets a blend.
    :param resource_path_root: Resource path
    """

    blend = ExcelBlendProposal(
        sheet=openpyxl.load_workbook(
            resource_path_root / BLEND_FILE_NAME
        ).active,
        bp_start_cell=FakeStartCell(row=7, column=6)
    )
    assert_that(
        blend.date(),
        equal_to(date(2022, 10, 7)),
        "Blend proposal date should match"
    )
    assert_that(
        len(blend.sequences().items()),
        equal_to(3),
        "Blend proposal sequences count should match"
    )

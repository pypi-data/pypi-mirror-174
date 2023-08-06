"""
Test case for blend sequence from PostgreSQL.
.. since: 0.5
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
import sqlalchemy  # type: ignore
from hamcrest import assert_that, equal_to, is_,\
    contains_inanyorder, has_length

from edv_dwh_connector.blend_proposal.db.pg_blend_sequence \
    import PgBlendSequence, PgBlendSequences
from edv_dwh_connector.blend_proposal.excel.blend_proposal_start_cell \
    import BlendProposalStartCell
from edv_dwh_connector.blend_proposal.excel.blend_sequence_start_cell \
    import BlendSequenceStartCell
from edv_dwh_connector.blend_proposal.excel.excel_blend_sequence \
    import ExcelBlendSequence
from tests.adapted_postgresql import AdaptedPostreSQL, PgDwhForTests

BLEND_FILE_NAME = "3.Daily_Blend_Template_process_October.xlsx"


def test_gets_blend_sequence() -> None:
    """
    Test gets blend sequence.
    """

    with AdaptedPostreSQL() as postgres:
        sequence = PgBlendSequence(
            date(2022, 10, 7), 1,
            PgDwhForTests(
                sqlalchemy.create_engine(postgres.get_connection_url())
            )
        )
        assert_that(
            sequence.date(), equal_to(date(2022, 10, 7)),
            "Sequence date should match"
        )
        assert_that(
            sequence.order(), equal_to(1),
            "Sequence order should match"
        )
        assert_that(
            sequence.name(),
            equal_to("WHEN THE CRUSHER COME ON LINE"),
            "Sequence name should match"
        )
        assert_that(
            sequence.average_grade(),
            equal_to(2.268),
            "Sequence average grade should match"
        )
        assert_that(
            sequence.soluble_copper(),
            equal_to(465.394),
            "Sequence soluble copper should match"
        )
        assert_that(
            sequence.as_ppm(),
            equal_to(527.253),
            "Sequence arsenic should match"
        )
        assert_that(
            sequence.moisture_estimated(),
            equal_to(0.172),
            "Sequence moisture estimated should match"
        )
        assert_that(
            sequence.oxide_transition(),
            equal_to(0.475),
            "Sequence oxide/transition should match"
        )
        assert_that(
            sequence.fresh(),
            equal_to(0.525),
            "Sequence fresh should match"
        )
        assert_that(
            sequence.recovery_blend_estimated(),
            equal_to(0.838),
            "Sequence recovery blend should match"
        )
        assert_that(
            sequence.materials().items(),
            has_length(5),
            "Sequence materials count should match"
        )
        assert_that(
            [material.name() for material in sequence.materials().items()],
            contains_inanyorder(
                "VSM_LG_HG_AS", "LG_HG_OX_TR_HCU", "LEP_HG_FR_LCU",
                "SURGE_BIN_OX_LG_HG", "SURGE_BIN_FR_LG_HG"
            ),
            "Sequence materials names should match"
        )


def test_adds_new_blend_sequence(resource_path_root) -> None:
    """
    Test adds a blend sequence.
    :param resource_path_root: Resource path
    """

    with AdaptedPostreSQL() as postgres:
        sheet = openpyxl.load_workbook(
            resource_path_root / BLEND_FILE_NAME
        ).active
        bp_start_cell = BlendProposalStartCell(
            sheet=sheet, day=date(2022, 10, 7)
        )
        sequence = ExcelBlendSequence(
            sheet=sheet,
            order=1,
            bs_start_cell=BlendSequenceStartCell(
                sheet=sheet,
                bp_start_cell=bp_start_cell,
                number=1
            ),
            bp_start_cell=bp_start_cell
        )
        sequences = PgBlendSequences(
            date(2022, 10, 6),
            PgDwhForTests(
                sqlalchemy.create_engine(postgres.get_connection_url())
            )
        )
        new_sequence = sequences.add(sequence)
        assert_that(
            new_sequence.date(),
            equal_to(date(2022, 10, 6)),
            "Sequence date should match"
        )
        assert_that(
            new_sequence.order(), equal_to(1),
            "Sequence order should match"
        )
        assert_that(
            new_sequence.name(),
            equal_to("WHEN THE CRUSHER COME ON LINE"),
            "Sequence name should match"
        )
        assert_that(
            new_sequence.average_grade(),
            equal_to(2.268),
            "Sequence average grade should match"
        )
        assert_that(
            new_sequence.soluble_copper(),
            equal_to(465.394),
            "Sequence soluble copper should match"
        )
        assert_that(
            new_sequence.as_ppm(),
            equal_to(527.253),
            "Sequence arsenic should match"
        )
        assert_that(
            new_sequence.moisture_estimated(),
            equal_to(0.172),
            "Sequence moisture estimated should match"
        )
        assert_that(
            new_sequence.oxide_transition(),
            equal_to(0.475),
            "Sequence oxide/transition should match"
        )
        assert_that(
            new_sequence.fresh(),
            equal_to(0.525),
            "Sequence fresh should match"
        )
        assert_that(
            new_sequence.recovery_blend_estimated(),
            equal_to(0.838),
            "Sequence recovery blend should match"
        )
        assert_that(
            new_sequence.materials().items(),
            has_length(6),
            "Sequence materials count should match"
        )
        assert_that(
            [material.name() for material in new_sequence.materials().items()],
            contains_inanyorder(
                "VSM_LG_HG_AS", "LG_HG_OX_TR_HCU", "LG_OX_TR_LCU",
                "LEP_HG_FR_LCU", "SURGE_BIN_OX_LG_HG", "SURGE_BIN_FR_LG_HG"
            ),
            "Sequence materials names should match"
        )
        assert_that(
            sequences.has("WHEN THE CRUSHER COME ON LINE"), is_(True),
            "Sequences should have new sequence"
        )
        assert_that(
            sequences.get("WHEN THE CRUSHER COME ON LINE").name(),
            equal_to("WHEN THE CRUSHER COME ON LINE"),
            "Sequences should get new sequence by its name"
        )
        assert_that(
            sequences.items(), has_length(1),
            "Sequences size should match"
        )

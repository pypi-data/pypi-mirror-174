"""
Test case for blend material from PostgreSQL.
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

# pylint: disable=duplicate-code
from datetime import date
import openpyxl  # type: ignore
import sqlalchemy  # type: ignore
from hamcrest import assert_that, equal_to, is_, has_length
from edv_dwh_connector.blend_proposal.db.pg_blend_material\
    import PgBlendMaterial, PgBlendMaterials
from edv_dwh_connector.blend_proposal.excel.blend_proposal_start_cell \
    import BlendProposalStartCell
from edv_dwh_connector.blend_proposal.excel.blend_sequence_start_cell \
    import BlendSequenceStartCell
from edv_dwh_connector.blend_proposal.excel.excel_blend_material \
    import ExcelBlendMaterial
from edv_dwh_connector.blend_proposal.excel.blend_material_start_cell \
    import BlendMaterialStartCell
from tests.adapted_postgresql import AdaptedPostreSQL, PgDwhForTests

BLEND_FILE_NAME = "3.Daily_Blend_Template_process_October.xlsx"


def test_gets_blend_material() -> None:
    """
    Test gets blend material.
    """

    with AdaptedPostreSQL() as postgres:
        material = PgBlendMaterial(
            date(2022, 10, 7), 1, "LG_HG_OX_TR_HCU",
            PgDwhForTests(
                sqlalchemy.create_engine(postgres.get_connection_url())
            )
        )
        assert_that(
            material.name(),
            equal_to("LG_HG_OX_TR_HCU"),
            "Material name should match"
        )
        assert_that(
            material.machine_type(),
            equal_to("CRUSHER"),
            "Material machine type should match"
        )
        assert_that(
            material.pit(),
            equal_to("WAL/BAK"),
            "Material pit should match"
        )
        assert_that(
            material.au_grade(),
            equal_to(2.034),
            "Material au grade should match"
        )
        assert_that(
            material.sol_cu(),
            equal_to(1114.728),
            "Material soluble copper should match"
        )
        assert_that(
            material.as_ppm(),
            equal_to(92.965),
            "Material arsenic should match"
        )
        assert_that(
            material.moisture(),
            equal_to(0.12),
            "Material moisture should match"
        )
        assert_that(
            material.indicative_rec(),
            equal_to(0.928),
            "Material indicative rec should match"
        )
        assert_that(
            material.bucket(),
            equal_to(1.465),
            "Material bucket should match"
        )
        assert_that(
            material.available_tons(),
            equal_to(2226.190),
            "Material available tons should match"
        )
        assert_that(
            material.prop(),
            equal_to(0.1),
            "Material prop should match"
        )


def test_adds_new_blend_material(resource_path_root) -> None:
    """
    Test adds a blend material.
    :param resource_path_root: Resource path
    """

    with AdaptedPostreSQL() as postgres:
        sheet = openpyxl.load_workbook(
            resource_path_root / BLEND_FILE_NAME
        ).active
        material = ExcelBlendMaterial(
            sheet=sheet,
            bs_start_cell=BlendSequenceStartCell(
                sheet=sheet,
                bp_start_cell=BlendProposalStartCell(
                    sheet=sheet, day=date(2022, 10, 7)
                ),
                number=3
            ),
            sm_start_cell=BlendMaterialStartCell(row=47, column=9)
        )
        materials = PgBlendMaterials(
            date(2022, 10, 7), 3,
            PgDwhForTests(
                sqlalchemy.create_engine(postgres.get_connection_url())
            )
        )
        new_material = materials.add(material)
        assert_that(
            new_material.name(),
            equal_to("VSM_LG_HG_AS"),
            "Material name should match"
        )
        assert_that(
            new_material.machine_type(),
            equal_to("CRUSHER"),
            "Material machine type should match"
        )
        assert_that(
            new_material.pit(),
            equal_to("DAAPLEU"),
            "Material pit should match"
        )
        assert_that(
            new_material.au_grade(),
            equal_to(3.47),
            "Material au grade should match"
        )
        assert_that(
            new_material.sol_cu(),
            equal_to(15),
            "Material soluble copper should match"
        )
        assert_that(
            new_material.as_ppm(),
            equal_to(2576.964),
            "Material arsenic should match"
        )
        assert_that(
            new_material.moisture(),
            equal_to(0.12),
            "Material moisture should match"
        )
        assert_that(
            new_material.indicative_rec(),
            equal_to(0.593),
            "Material indicative rec should match"
        )
        assert_that(
            new_material.bucket(),
            equal_to(1),
            "Material bucket should match"
        )
        assert_that(
            new_material.available_tons(),
            equal_to(5568),
            "Material available tons should match"
        )
        assert_that(
            new_material.prop(),
            equal_to(1),
            "Material prop should match"
        )
        assert_that(
            materials.has("VSM_LG_HG_AS"), is_(True),
            "Materials should have new material"
        )
        assert_that(
            materials.get("VSM_LG_HG_AS").name(), equal_to("VSM_LG_HG_AS"),
            "Materials should get new material by its name"
        )
        assert_that(
            materials.items(), has_length(1),
            "Materials size should match"
        )

"""
Test case for cached PITag.
.. since: 0.4
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
import sqlalchemy  # type: ignore
from hamcrest import assert_that, equal_to, raises, calling
from edv_dwh_connector.pi.db.pg_pi_tag import PgCachedPITags
from tests.adapted_postgresql import AdaptedPostreSQL, PgDwhForTests


WEB_ID = "F1DSmN2338899MpX8PREOtdbEZ56sypASVRZLVNSVi1QSS1ISTAx"


def test_tries_to_save_new_tag() -> None:
    """
    Tests that it doesn't manage tag creation.
    """

    with AdaptedPostreSQL() as postgres:
        tags = PgCachedPITags(
            PgDwhForTests(
                sqlalchemy.create_engine(postgres.get_connection_url())
            )
        )
        assert_that(
            calling(tags.add).with_args(
                "AI160014A_SCLD",
                "CIL Free Cyanide Analyser pH Indicator Tank 1 Scaled Value",
                "pH", WEB_ID
            ),
            raises(
                NotImplementedError,
                "We can't add new tag to a cached list"
            ),
            "Should not be able to create a new tag"
        )


def test_gets_tag_by_code() -> None:
    """
    Gets tag by code.
    """

    with AdaptedPostreSQL() as postgres:
        tags = PgCachedPITags(
            PgDwhForTests(
                sqlalchemy.create_engine(postgres.get_connection_url())
            )
        )
        code = "AI162003_SCLD"
        assert_that(
            tags.get(code).code(), equal_to(code),
            "Cached PI Tags should get a tag by its code"
        )


def test_lists_tags() -> None:
    """
    Lists tags.
    """

    with AdaptedPostreSQL() as postgres:
        tags = PgCachedPITags(
            PgDwhForTests(
                sqlalchemy.create_engine(postgres.get_connection_url())
            )
        )
        codes = ['AI162003_SCLD', 'AI162007_SCLD', 'AI162014_SCLD']
        for idx, tag in enumerate(tags.items()):
            assert_that(
                tag.code(), equal_to(codes[idx]),
                "Tag from cached PI Tags should should match code"
            )

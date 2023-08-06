"""
Test case for cached PI tag measures.
.. since: 0.2
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
from datetime import datetime

# pylint: disable=duplicate-code
import sqlalchemy  # type: ignore
from hamcrest import assert_that, equal_to, calling, raises
from edv_dwh_connector.pi.db.pg_pi_tag import PgPITags
from edv_dwh_connector.pi.db.pg_pi_measure import PgPIMeasures,\
    PgCachedPIMeasures
from tests.adapted_postgresql import AdaptedPostreSQL, \
    PgDwhForTests


def test_tries_to_save_new_measure() -> None:
    """
    Tests that it doesn't save a measure.
    """

    with AdaptedPostreSQL() as postgres:
        engine = sqlalchemy.create_engine(postgres.get_connection_url())
        dwh = PgDwhForTests(engine)
        tag_code = "AI162003_SCLD"
        date = datetime(
            year=2022, month=1, day=15,
            hour=12, minute=55, second=30, microsecond=177990
        )
        tag = PgPITags(dwh).get(tag_code)
        PgPIMeasures(tag, dwh).add(date=date, value=35.71)
        measure = PgCachedPIMeasures(tag, dwh).items(date, date)[0]
        assert_that(
            measure.tag().code(), equal_to(tag_code),
            "Cached measure PI Tag should match"
        )
        assert_that(
            datetime.strptime(
                measure.date().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                "%Y-%m-%d %H:%M:%S.%f"
            ), equal_to(
                datetime.strptime(
                    date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    "%Y-%m-%d %H:%M:%S.%f"
                )
            ),
            "Cached PI Tag measure date should match"
        )
        assert_that(
            measure.value(), equal_to(35.71),
            "Cached PI Tag measure value should match"
        )


def test_lists_items() -> None:
    """
    Tests that it lists items.
    """

    with AdaptedPostreSQL() as postgres:
        date = datetime(
            year=2022, month=1, day=19,
            hour=15, minute=7, second=12, microsecond=177990
        )
        dwh = PgDwhForTests(
            sqlalchemy.create_engine(postgres.get_connection_url())
        )
        tag = PgPITags(dwh).get("AI162003_SCLD")
        PgPIMeasures(tag, dwh).add(date=date, value=35.71)
        measures = PgCachedPIMeasures(tag, dwh)
        assert_that(
            len(measures.items(date, date)), equal_to(1),
            "Cached measures of PI Tag should be retrieved"
        )
        assert_that(
            len(measures.items(date.now(), date.now())), equal_to(0),
            "Cached measures of PI Tag should be empty"
        )


def test_lists_items_of_tag_code() -> None:
    """
    Tests that it lists items from tag code.
    """

    with AdaptedPostreSQL() as postgres:
        date = datetime(
            year=2022, month=1, day=20, hour=11, minute=20, second=0
        )
        dwh = PgDwhForTests(
            sqlalchemy.create_engine(postgres.get_connection_url())
        )
        tag = PgPITags(dwh).get("AI162014_SCLD")
        PgPIMeasures(tag, dwh).add(date=date, value=78.01)
        measures = PgCachedPIMeasures.of_tag_code(tag.code(), dwh)
        assert_that(
            len(measures.items(date, date)), equal_to(1),
            "Cached measures from PI Tag code should be retrieved"
        )
        assert_that(
            len(measures.items(date.now(), date.now())), equal_to(0),
            "Cached measures from PI Tag code should be empty"
        )


def test_tries_to_check_existence_at_a_date() -> None:
    """
    Tests that it doesn't manage existence checking.
    """

    with AdaptedPostreSQL() as postgres:
        dwh = PgDwhForTests(
            sqlalchemy.create_engine(postgres.get_connection_url())
        )
        measures = PgCachedPIMeasures(
            PgPITags(dwh).get("AI162003_SCLD"), dwh
        )
        assert_that(
            calling(measures.has_at).with_args(datetime(2022, 7, 1)),
            raises(
                NotImplementedError,
                "We are not able to check now existence "
                "of a measure in a cached list"
            ),
            "Should not be able to check measure existence at a date"
        )

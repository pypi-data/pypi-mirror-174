"""
Test case for hour intervals.
.. since: 0.6
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
from datetime import datetime
from hamcrest import assert_that, is_, calling, raises
from edv_dwh_connector.utils.periods import \
    SimplePeriod, HourIntervals


def are_equal_to(actual: list, expected: list) -> bool:
    """
    Checks that periods are equal.
    :param actual: Actual periods
    :param expected: Periods expected
    :return: Are equal or not
    """
    if len(actual) == len(expected)\
            and (len(expected) == 0 or len(expected) > 0):
        matches = True
    else:
        matches = False
        print(
            f"Length of periods doesn't match :"
            f" actual -> {len(actual)}, expected -> {len(expected)}"
        )
    if matches:
        for idx, act in enumerate(actual):
            if not (
                # pylint: disable=line-too-long
                act.start() == expected[idx].start() and act.end() == expected[idx].end()  # noqa: E501
            ):
                print(
                    f"Periods [{act.start()}, {act.end()}]"
                    f" and [{expected[idx].start()}, {expected[idx].end()}]"
                    " don't match"
                )
                matches = False
                break
    return matches


def test_generates_hour_intervals_on_long_period() -> None:
    """
    Tests that we generate day intervals on period upper than a day.
    """
    periods = HourIntervals(
        datetime(2022, 10, 11, 5, 10, 2),
        datetime(2022, 10, 11, 10, 10, 2)
    )
    expected = [
        SimplePeriod(
            datetime(2022, 10, 11, 5, 10, 2), datetime(2022, 10, 11, 6, 10, 1)
        ),
        SimplePeriod(
            datetime(2022, 10, 11, 6, 10, 2), datetime(2022, 10, 11, 7, 10, 1)
        ),
        SimplePeriod(
            datetime(2022, 10, 11, 7, 10, 2), datetime(2022, 10, 11, 8, 10, 1)
        ),
        SimplePeriod(
            datetime(2022, 10, 11, 8, 10, 2), datetime(2022, 10, 11, 9, 10, 1)
        ),
        SimplePeriod(
            datetime(2022, 10, 11, 9, 10, 2), datetime(2022, 10, 11, 10, 10, 2)
        )
    ]
    assert_that(
        are_equal_to(periods.items(), expected), is_(True),
        "Intervals generated on long period should match"
    )


def test_generates_hour_intervals_on_short_period() -> None:
    """
    Tests that we generate hour intervals on period less than an hour.
    """
    periods = HourIntervals(
        datetime(2022, 10, 10, 5, 0, 0),
        datetime(2022, 10, 10, 6, 0, 0)
    )
    expected = [
        SimplePeriod(
            datetime(2022, 10, 10, 5, 0, 0), datetime(2022, 10, 10, 6, 0, 0)
        )
    ]
    assert_that(
        are_equal_to(periods.items(), expected), is_(True),
        "Intervals generated on short period should match"
    )


def test_generates_hour_intervals_on_same_dates() -> None:
    """
    Tests that we generate day intervals on period of same date.
    """
    periods = HourIntervals(
        datetime(2022, 10, 10, 5, 0, 0),
        datetime(2022, 10, 10, 5, 0, 0)
    )
    expected = [
        SimplePeriod(
            datetime(2022, 10, 10, 5, 0, 0), datetime(2022, 10, 10, 5, 0, 0)
        )
    ]
    assert_that(
        are_equal_to(periods.items(), expected), is_(True),
        "Intervals generated on same dates should match"
    )


def generate_intervals(start: datetime, end: datetime) -> None:
    """
    Generates intervals.
    :param start: Start date
    :param end: End date
    """
    HourIntervals(start, end).items()


def test_generates_hour_intervals_on_wrong_period() -> None:
    """
    Tests that we generate hour intervals on wrong period.
    """
    assert_that(
        calling(generate_intervals).with_args(
            datetime(2022, 10, 10, 5, 0, 0),
            datetime(2022, 10, 9, 5, 0, 0)
        ),
        raises(
            ValueError,
            "Bad range, dates are equals or start date"
            " is greater than end date"
        ),
        "Should not generate intervals on wrong period"
    )

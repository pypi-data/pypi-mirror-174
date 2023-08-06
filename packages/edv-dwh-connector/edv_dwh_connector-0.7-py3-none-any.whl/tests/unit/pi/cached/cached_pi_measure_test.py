"""
Test case for CachedPIMeasure.
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

from datetime import datetime
from hamcrest import assert_that, equal_to
from edv_dwh_connector.pi.cached.cached_pi_tag import CachedPITag
from edv_dwh_connector.pi.cached.cached_pi_measure import CachedPIMeasure


def test_caches_a_measure() -> None:
    """
    Test that measure caches well.
    """
    date = datetime(2022, 1, 1, 7, 5, 0)
    value = 10.1
    measure = CachedPIMeasure(
        tag=CachedPITag(
            uid=1, code="AI160014A_SCLD",
            name="AI160014A CIL Free Cyanide Analyser "
            "pH Indicator Tank 1 Scaled Value",
            uom="pH",
            web_id="F1DPmN2MpX8PREOtdbEZ56sypAQw"
            "IAAASVRZLVNSVi1QSS1ISTAxXEFJMTYwMDE0QV9TQ0xE"
        ),
        date=date, value=value
    )
    assert_that(
        measure.tag().uid(), equal_to(1),
        "Cached measure tag should match"
    )
    assert_that(
        measure.date(), equal_to(date),
        "Cached measure should match date"
    )
    assert_that(
        measure.value(), equal_to(value),
        "Cached measure should match value"
    )

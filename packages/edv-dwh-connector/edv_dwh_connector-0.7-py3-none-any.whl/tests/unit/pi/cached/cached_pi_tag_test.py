"""
Test case for CachedPITag.
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

from hamcrest import assert_that, equal_to
from edv_dwh_connector.pi.cached.cached_pi_tag import CachedPITag


def test_caches_a_pi_tag() -> None:
    """
    Tests that tag is cached well.
    """
    uid = 1
    code = "AI160014A_SCLD"
    name = "AI160014A CIL Free Cyanide Analyser " \
        "pH Indicator Tank 1 Scaled Value"
    uom = "pH"
    web_id = "F1DPmN2MpX8PREOtdbEZ56sypAQwIAAASVRZL" \
        "VNSVi1QSS1ISTAxXEFJMTYwMDE0QV9TQ0xE"
    tag = CachedPITag(uid, code, name, uom, web_id)
    assert_that(
        tag.uid(), equal_to(uid),
        "Cached tag should match UID"
    )
    assert_that(
        tag.code(), equal_to(code),
        "Cached tag should match code"
    )
    assert_that(
        tag.name(), equal_to(name),
        "Cached tag should match name"
    )
    assert_that(
        tag.uom(), equal_to(uom),
        "Cached tag should match UOM"
    )
    assert_that(
        tag.web_id(), equal_to(web_id),
        "Cached tag should match Web ID"
    )

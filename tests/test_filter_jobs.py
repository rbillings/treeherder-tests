# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.treeherder import TreeherderPage


@pytest.mark.nondestructive
def test_filter_jobs(base_url, selenium):
    """Open resultset page and filter for platform"""
    term = u'Linux'
    page = TreeherderPage(base_url, selenium).open()
    page.filter_search(term)
    assert "&filter-searchStr=Linux" in page.selenium.current_url

    """Clear filter results"""
    page.filter_clear()
    assert "&filter-searchStr=Linux" not in page.selenium.current_url

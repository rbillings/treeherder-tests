# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from selenium.webdriver.common.by import By

from pages.treeherder import TreeherderPage


class TestSingleResult:

    @pytest.mark.nondestructive
    def test_open_single_result(self, base_url, selenium):

        treeherder_page = TreeherderPage(base_url, selenium).open()
        revision_date = treeherder_page.first_revision_date
        single_result_page = treeherder_page.open_single_resultset()
        assert 1 == single_result_page.results_count
        assert revision_date == single_result_page.revision_date

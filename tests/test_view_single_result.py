# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.treeherder import TreeherderPage


class TestSingleResult:

    @pytest.mark.nondestructive
    def test_open_single_result(self, base_url, selenium):
        page = TreeherderPage(base_url, selenium).open()
        first_revision_date = page.first_revision_date
        page.open_single_resultset()
        assert 1 == page.results_count
        assert first_revision_date == page.first_revision_date

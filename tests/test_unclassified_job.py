# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.treeherder import TreeherderPage


class TestUnclassifiedJobs:

    @pytest.mark.nondestructive
    def test_unclassified_failure(self, base_url, selenium):
        """ Open resultset page and search for next unclassified failure"""
        page = TreeherderPage(base_url, selenium).open()
        assert page.unclassified_failure_count > 0

        page.open_next_unclassified_failure()
        teststatus = page.result.job_result_status
        assert teststatus in ['busted', 'testfailed', 'exception']

    @pytest.mark.nondestructive
    def test_open_unclassified_failure_log(self, base_url, selenium):
        """ Open the job log and verify there is content """
        treeherder_page = TreeherderPage(base_url, selenium).open()
        assert treeherder_page.unclassified_failure_count > 0
        treeherder_page.open_next_unclassified_failure()
        logviewer_page = treeherder_page.job_details.open_logviewer()
        assert logviewer_page.is_job_status_visible

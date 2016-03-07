# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.treeherder import TreeherderPage


class TestUnclassifiedJobs:

    def test_pin_next_job(self, base_url, selenium, new_user):
        # Open treeherder page, log in and pin a job
        page = TreeherderPage(base_url, selenium).open()
        page.header.login(new_user['email'], new_user['password'])
        assert page.header.is_user_logged_in

        next_job_title = page.select_next_job()
        page.add_selected_job_to_pinboard()

        assert next_job_title == page.pinned_job_title

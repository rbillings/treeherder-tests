# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.treeherder import TreeherderPage


class TestUnclassifiedJobs:

    def test_pin_next_job(self, base_url, selenium):
        # Open treeherder page, select next job and pin it
        page = TreeherderPage(base_url, selenium).open()

        next_job_title = page.select_next_job()
        page.add_selected_job_to_pinboard()

        assert next_job_title == page.pinned_job_title

    def test_pin_job_from_logviewer(self, base_url, selenium):
        # Open treeherder page, select next job, pin it by the logviewer icon
        page = TreeherderPage(base_url, selenium).open()

        next_job_title = page.select_next_job()
        page.pin_job_from_logviewer()

        assert next_job_title == page.pinned_job_title

    def test_clear_pinboard(self, base_url, selenium):
        # Open treeherder page, pin a job and then clear the pinboard
        page = TreeherderPage(base_url, selenium).open()

        page.select_next_job()
        page.add_selected_job_to_pinboard()
        page.clear_pinboard()

        assert not page.any_jobs_pinned

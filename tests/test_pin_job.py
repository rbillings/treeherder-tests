# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.treeherder import TreeherderPage


class TestPinJobs:

    def test_pin_next_job(self, base_url, selenium):
        """ Open treeherder page, select next job and pin it"""
        page = TreeherderPage(base_url, selenium).open()
        current_job_title = page.select_next_job()
        assert 0 == page.pinboard.pins
        page.result.pin_using_spacebar()
        assert 1 == page.pinboard.pins
        assert current_job_title in page.pinboard.pinned_job_title

    def test_pin_job_from_job_details(self, base_url, selenium):
        """ Open treeherder page, select next job, pin it by the logviewer icon"""
        page = TreeherderPage(base_url, selenium).open()

        next_job_title = page.select_next_job()
        assert 0 == page.pinboard.pins
        page.job_details.pin_job()
        assert 1 == page.pinboard.pins
        assert next_job_title in page.pinboard.pinned_job_title

    def test_clear_pinboard(self, base_url, selenium):
        """ Open treeherder page, pin a job and then clear the pinboard"""
        page = TreeherderPage(base_url, selenium).open()

        page.select_next_job()
        page.result.pin_using_spacebar()
        assert 1 == page.pinboard.pins
        page.pinboard.clear_pinboard()
        assert page.pinboard.is_pinboard_open
        assert 0 == page.pinboard.pins

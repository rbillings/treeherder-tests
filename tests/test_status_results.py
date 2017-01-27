# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import random

from pages.treeherder import TreeherderPage


@pytest.mark.nondestructive
def test_status_results(base_url, selenium):
    """Open resultset page and verify job status buttons in the nav"""
    page = TreeherderPage(selenium, base_url).open()
    page.filter_job_failures()
    page.filter_job_successes()
    page.filter_job_retries()
    page.filter_job_usercancel()
    page.filter_job_in_progress()

    all_jobs = page.all_jobs
    unfiltered_jobs = len(page.all_jobs)

    page.filter_job_failures()
    all_jobs = page.all_jobs
    job = random.choice(all_jobs)
    unclassified = ['testfailed', 'exception', 'busted']
    assert any(status in job.title for status in unclassified)

    page.filter_job_successes()
    page.filter_job_retries()
    page.filter_job_usercancel()
    page.filter_job_in_progress()

    all_jobs = page.all_jobs
    filtered_jobs = len(page.all_jobs)
    job = random.choice(all_jobs)
    all = ['testfailed', 'exception', 'busted', 'success','retry','coalesced','running']
    assert any(status in job.title for status in all)
    assert filtered_jobs > unfiltered_jobs

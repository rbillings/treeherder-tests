# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.treeherder import TreeherderPage


@pytest.mark.nondestructive
def test_add_new_jobs(base_url, selenium):
    page = TreeherderPage(selenium, base_url).open()
    assert len(page.result_sets) >= 1
    page.result_sets[0].view()
    page.result_sets[0].add_new_jobs()
    assert len(page.result_sets[0].runnable_jobs) > 0


@pytest.mark.nondestructive
def test_hide_runnable_jobs(base_url, selenium):
    page = TreeherderPage(selenium, base_url).open()
    assert len(page.result_sets) >= 1
    page.result_sets[0].view()
    page.result_sets[0].add_new_jobs()
    assert len(page.result_sets[0].runnable_jobs) > 0
    page.result_sets[0].hide_runnable_jobs()
    assert len(page.result_sets[0].runnable_jobs) == 0

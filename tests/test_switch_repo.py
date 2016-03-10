# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.treeherder import TreeherderPage


@pytest.mark.nondestructive
def test_switch_repo(base_url, selenium):
    """ Switch to new active watched repo"""
    page = TreeherderPage(base_url, selenium).open()
    initial_repo = page.active_watched_repo
    new_repo = page.select_random_repo()
    assert initial_repo != new_repo
    assert new_repo == page.active_watched_repo

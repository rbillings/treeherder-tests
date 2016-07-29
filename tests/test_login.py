# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.treeherder import TreeherderPage


@pytest.mark.nondestructive
def test_that_a_new_user_can_login(base_url, selenium, new_user):
    page = TreeherderPage(selenium, base_url).open()
    page.header.login(new_user['email'], new_user['password'])
    assert page.header.is_user_logged_in

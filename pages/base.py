# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bidpom import BIDPOM
from pypom import Page, Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Base(Page):

    @property
    def header(self):
        return self.Header(self)

    class Header(Region):

        _root_locator = (By.ID, 'th-global-navbar')
        _login_locator = (By.CSS_SELECTOR, '.nav-login-btn > span:nth-child(1)')
        _logout_icon_locator = (By.ID, 'logoutLabel')
        _dropdown_menu_switch_page_locator = (By.CSS_SELECTOR, '.open ul > li a')
        _dropdown_menu_locator = (By.ID, 'th-logo')

        @property
        def is_user_logged_in(self):
            return self.is_element_displayed(*self._logout_icon_locator)

        def click_login(self):
            self.find_element(*self._login_locator).click()

        def login(self, email, password):
            self.click_login()
            browser_id = BIDPOM(self.selenium, self.timeout)
            browser_id.sign_in(email, password)
            self.wait.until(EC.visibility_of_element_located(self._logout_icon_locator))

        def switch_page_using_dropdown(self):
            self.find_element(*self._dropdown_menu_locator).click()
            self.find_element(*self._dropdown_menu_switch_page_locator).click()

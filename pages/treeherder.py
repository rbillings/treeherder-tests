# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait

import expected
import random
from pages.base import Base
from pages.page import Page


class TreeherderPage(Base):

    _active_watched_repo = (By.CSS_SELECTOR, '#watched-repo-navbar button.active')
    _job_details_actionbar_locator = (By.ID, 'job-details-actionbar')
    _job_result_status_locator = (By.CSS_SELECTOR, '#result-status-pane > div:nth-child(1) > span')
    _logviewer_button_locator = (By.ID, 'logviewer-btn')
    _repos_menu_locator = (By.ID, 'repoLabel')
    _repos_links_locator = (By.CSS_SELECTOR, '#repoLabel + .dropdown-menu .dropdown-checkbox:not([checked]) + .dropdown-link')
    _repos_specific_locator = (By.CSS_SELECTOR, '.dropdown-link a')
    _resultset_locator = (By.CSS_SELECTOR, 'div.row.result-set')
    _result_status_locator = (By.ID, 'job-details-panel')
    _unclassified_failure_count_locator = (By.ID, 'unclassified-failure-count')

    def wait_for_page_to_load(self):
        Wait(self.selenium, self.timeout).until(
            lambda s: self.unclassified_failure_count > 0)
        return self

    @property
    def active_watched_repo(self):
        return self.selenium.find_element(*self._active_watched_repo).text

    @property
    def job_result_status(self):
        return self.selenium.find_element(*self._job_result_status_locator).text

    @property
    def unclassified_failure_count(self):
        return int(self.selenium.find_element(*self._unclassified_failure_count_locator).text)

    def open_next_unclassified_failure(self):
        el = self.selenium.find_element(*self._resultset_locator)
        Wait(self.selenium, self.timeout).until(EC.visibility_of(el))
        el.send_keys('n')
        Wait(self.selenium, self.timeout).until(lambda s: self.job_result_status)

    def open_logviewer(self):
        Wait(self.selenium, self.timeout).until(
            EC.visibility_of_element_located(self._job_details_actionbar_locator))
        self.selenium.find_element(*self._resultset_locator).send_keys('l')
        return LogviewerPage(self.base_url, self.selenium)

    def open_perfherder_page(self):
        self.header.switch_page_using_dropdown()

        from perfherder import PerfherderPage
        return PerfherderPage(self.base_url, self.selenium).wait_for_page_to_load()

    def open_repos_menu(self):
        self.selenium.find_element(*self._repos_menu_locator).click()

    def select_random_repo(self):
        self.selenium.open_repos_menu()
        random.choice(unchecked_repos_links).click()
        self.wait_for_page_to_load
        return self.active_watched_repo

    def select_specific_repo(self, repo):
        self.open_repos_menu()
        self.selenium.find_element(By.LINK_TEXT, repo).click()
        self.wait_for_page_to_load
        return self.active_watched_repo

class LogviewerPage(Page):

    _job_header_locator = (By.CSS_SELECTOR, 'div.job-header')

    def __init__(self, base_url, selenium):
        Page.__init__(self, base_url, selenium)
        Wait(self.selenium, self.timeout).until(
            expected.window_with_title('Log for'))

    @property
    def is_job_status_visible(self):
        return self.is_element_visible(self._job_header_locator)

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait

import expected
from pages.base import Base
from pages.page import Page


class TreeherderPage(Base):

    _first_resultset_locator = (By.CSS_SELECTOR, '.th-view-content > ng-view:nth-child(1) > div:nth-child(2) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1) > span:nth-child(2) > a:nth-child(1)')
    _first_resultset_datestamp_locator = (By.CSS_SELECTOR, '.result-set .result-set-title-left > span a')
    _job_details_actionbar_locator = (By.ID, 'job-details-actionbar')
    _job_result_status_locator = (By.CSS_SELECTOR, '#result-status-pane > div:nth-child(1) > span')
    _logviewer_button_locator = (By.ID, 'logviewer-btn')
<<<<<<< 96097695cdecedfef212f6b55624f12978ef91d9:pages/treeherder.py
    _resultset_locator = (By.CSS_SELECTOR, 'div.row.result-set')
=======
    _resultset_datestamp_locator = (By.CSS_SELECTOR, '.result-set .result-set-title-left > span a')
    _result_status_locator = (By.ID, 'job-details-panel')
>>>>>>> Updated datestamp locator:pages/resultset.py
    _unclassified_failure_count_locator = (By.ID, 'unclassified-failure-count')

    def wait_for_page_to_load(self):
        Wait(self.selenium, self.timeout).until(
            lambda s: self.unclassified_failure_count > 0)
        return self

    @property
    def job_result_status(self):
        return self.selenium.find_element(*self._job_result_status_locator).text

    @property
    def unclassified_failure_count(self):
        return int(self.selenium.find_element(*self._unclassified_failure_count_locator).text)

    @property
    def first_revision_date(self):
        return self.selenium.find_element(*self._first_resultset_datestamp_locator).text

    def open_next_unclassified_failure(self):
        el = self.selenium.find_element(*self._resultset_datestamp_locator)
        Wait(self.selenium, self.timeout).until(EC.visibility_of(el))
        el.send_keys('n')
        Wait(self.selenium, self.timeout).until(lambda s: self.job_result_status)

    def open_logviewer(self):
        Wait(self.selenium, self.timeout).until(
            EC.visibility_of_element_located(self._job_details_actionbar_locator))
        self.selenium.find_element(*self._first_resultset_datestamp_locator).send_keys('l')
        return LogviewerPage(self.base_url, self.selenium)

    def open_perfherder_page(self):
        self.header.switch_page_using_dropdown()

        from perfherder import PerfherderPage
        return PerfherderPage(self.base_url, self.selenium).wait_for_page_to_load()

    def open_single_resultset(self):
        Wait(self.selenium, self.timeout).until(
            EC.visibility_of_element_located(self._first_resultset_datestamp_locator))
        self.selenium.find_element(*self._first_resultset_datestamp_locator).click()
        return SingleResultPage(self.base_url, self.selenium)


class LogviewerPage(Page):

    _job_header_locator = (By.CSS_SELECTOR, 'div.job-header')

    def __init__(self, base_url, selenium):
        Page.__init__(self, base_url, selenium)
        Wait(self.selenium, self.timeout).until(
            expected.window_with_title('Log for'))

    @property
    def is_job_status_visible(self):
        return self.is_element_visible(self._job_header_locator)


class SingleResultPage(Page):

    _results_locator = (By.CSS_SELECTOR, '.result-set-bar')
    _single_resultset_datestamp_locator = (By.CSS_SELECTOR, '.result-set-title-left > span:nth-child(2) > a:nth-child(1)')

    def __init__(self, base_url, selenium):
        Page.__init__(self, base_url, selenium)
        Wait(self.selenium, self.timeout).until(
            expected.window_with_title('mozilla-inbound'))

    @property
    def revision_date(self):
        return self.selenium.find_element(*self._single_resultset_datestamp_locator).text

    @property
    def results_count(self):
        return len(self.selenium.find_elements(*self._results_locator))

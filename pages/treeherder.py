# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.keys import Keys

import expected
from pages.base import Base
from pages.page import Page
from pages.page import PageRegion


class TreeherderPage(Base):

    _clear_all_menu_locator = (By.CSS_SELECTOR, '#pinboard-controls .dropdown-menu li:nth-child(4)')
    _first_resultset_datestamp_locator = (By.CSS_SELECTOR, '.result-set .result-set-title-left > span a')
    _job_details_actionbar_locator = (By.ID, 'job-details-actionbar')
    _job_details_pin_job_locator = (By.CSS_SELECTOR, '#job-details-actionbar .nav .nav li:nth-child(1) a')
    _job_result_status_locator = (By.CSS_SELECTOR, '#result-status-pane > div:nth-child(1) > span')
    _logviewer_button_locator = (By.ID, 'logviewer-btn')
    _open_save_menu_locator = (By.CSS_SELECTOR, '#pinboard-controls .dropdown-toggle')
    _pinboard_count = (By.CSS_SELECTOR, '#pinned-job-list')
    _pinboard_locator = (By.ID, 'pinboard-panel')
    _pinboard_remove_job_locator = (By.CSS_SELECTOR, '#pinned-job-list .pinned-job-close-btn')
    _pinned_job_title_locator = (By.CSS_SELECTOR, '.pinned-job.selected-job')
    _resultset_locator = (By.CSS_SELECTOR, 'div.row.result-set')
    _result_status_locator = (By.ID, 'job-details-panel')
    _results_locator = (By.CSS_SELECTOR, '.result-set-bar')
    _selected_job_title_locator = (By.CSS_SELECTOR, '.job-list .selected-job')
    _result_set_locator = (By.CSS_SELECTOR, '#th-global-content .result-set')
    _unclassified_failure_count_locator = (By.ID, 'unclassified-failure-count')

    def wait_for_page_to_load(self):
        Wait(self.selenium, self.timeout).until(
            lambda s: self.unclassified_failure_count > 0)
        return self

    @property
    def result(self):
        return self.Result(self)

    @property
    def job_details(self):
        return self.JobDetails(self)

    @property
    def pinboard(self):
        return self.Pinboard(self)

    @property
    def unclassified_failure_count(self):
        return int(self.selenium.find_element(*self._unclassified_failure_count_locator).text)

    @property
    def first_revision_date(self):
        return self.selenium.find_element(*self._first_resultset_datestamp_locator).text

    @property
    def results_count(self):
        return len(self.selenium.find_elements(*self._results_locator))

    def open_next_unclassified_failure(self):
        el = self.selenium.find_element(*self._result_set_locator)
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

    def select_next_job(self):
        el = self.selenium.find_element(*self._resultset_locator)
        Wait(self.selenium, self.timeout).until(EC.visibility_of(el))
        el.send_keys(Keys.ARROW_RIGHT)
        Wait(self.selenium, self.timeout).until(lambda s: self.job_result_status)
        return self.selenium.find_element(*self._selected_job_title_locator).get_attribute('title')


    class Result(PageRegion):

        _job_result_status_locator = (By.CSS_SELECTOR, '#result-status-pane > div:nth-child(1) > span')
        _result_set_locator = (By.CSS_SELECTOR, '#th-global-content .result-set')
        _selected_job_title_locator = (By.CSS_SELECTOR, '.job-list .selected-job')

        @property
        def job_result_status(self):
            return self.selenium.find_element(*self._job_result_status_locator).text

        @property
        def result(self):
            return [Result(self, root=el) for el in
                self.find_elements(self._result_set_locator)]

        def pin_using_spacebar(self):
            el = self.selenium.find_element(*self._result_set_locator)
            Wait(self.selenium, self.timeout).until(EC.visibility_of(el))
            el.send_keys(Keys.SPACE)
            Wait(self.selenium, self.timeout).until(lambda s: self.pinboard.is_pinboard_open)

        def select_next_job(self):
            el = self.selenium.find_element(*self._result_set_locator)
            Wait(self.selenium, self.timeout).until(EC.visibility_of(el))
            el.send_keys(Keys.ARROW_RIGHT)
            Wait(self.selenium, self.timeout).until(lambda s: self.job_result_status)
            return self.selenium.find_element(*self._selected_job_title_locator).get_attribute('title')

    class JobDetails(PageRegion):

        _job_details_actionbar_locator = (By.ID, 'job-details-actionbar')
        _job_details_pin_job_locator = (By.CSS_SELECTOR, '#job-details-actionbar .nav .nav li:nth-child(1) a')
        _logviewer_button_locator = (By.ID, 'logviewer-btn')
        _result_status_locator = (By.ID, 'job-details-panel')

        def open_logviewer(self):
            Wait(self.selenium, self.timeout).until(
                EC.visibility_of_element_located(self._job_details_actionbar_locator))
            self.selenium.find_element(*self._result_set_locator).send_keys('l')
            return LogviewerPage(self.base_url, self.selenium)

        def pin_job(self):
            el = Wait(self.selenium, self.timeout).until(
                EC.visibility_of_element_located(self._job_details_actionbar_locator))
            el.find_element(*self._job_details_pin_job_locator).click()
            from pages.treeherder.pinboard import Pinboard
            return Pinboard(self.base_url, self.selenium)


    class Pinboard(PageRegion):

        _clear_all_menu_locator = (By.CSS_SELECTOR, '#pinboard-controls .dropdown-menu li:nth-child(4)')
        _open_save_menu_locator = (By.CSS_SELECTOR, '#pinboard-controls .dropdown-toggle')
        _pinboard_count = (By.CSS_SELECTOR, '#pinned-job-list')
        _pinboard_locator = (By.ID, 'pinboard-panel')
        _pinboard_remove_job_locator = (By.CSS_SELECTOR, '#pinned-job-list .pinned-job-close-btn')
        _pinned_job_title_locator = (By.CSS_SELECTOR, '.pinned-job.selected-job')

        @property
        def pinned_job_title(self):
            return self.selenium.find_element(*self._pinned_job_title_locator).get_attribute('title')

        @property
        def pins(self):
            return len(self.selenium.find_elements(*self._pinboard_count))

        @property
        def is_pinboard_open(self):
            return self.is_element_visible(self._pinboard_locator)

        def clear_pinboard(self):
            self.selenium.find_element(*self._open_save_menu_locator).click()
            self.selenium.find_element(*self._clear_all_menu_locator).click()


class LogviewerPage(Page):

    _job_header_locator = (By.CSS_SELECTOR, 'div.job-header')

    def __init__(self, base_url, selenium):
        Page.__init__(self, base_url, selenium)
        Wait(self.selenium, self.timeout).until(
            expected.window_with_title('Log for'))

    @property
    def is_job_status_visible(self):
        return self.is_element_visible(self._job_header_locator)

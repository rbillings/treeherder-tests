# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import itertools
import random

from pypom import Page, Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from pages.base import Base


class TreeherderPage(Base):

    _active_watched_repo_locator = (By.CSS_SELECTOR, '#watched-repo-navbar button.active')
    _clear_filter_locator = (By.ID, 'quick-filter-clear-button')
    _close_the_job_panel_locator = (By.CSS_SELECTOR, '.info-panel-navbar-controls > li:nth-child(2)')
    _filter_panel_all_failures_locator = (By.CSS_SELECTOR, '.pull-right input')
    _filter_panel_busted_failures_locator = (By.ID, 'busted')
    _filter_panel_exception_failures_locator = (By.ID, 'exception')
    _filter_panel_locator = (By.CSS_SELECTOR, 'span.navbar-right > span:nth-child(4)')
    _filter_panel_reset_locator = (By.CSS_SELECTOR, '.pull-right span:nth-child(3)')
    _filter_panel_testfailed_failures_locator = (By.ID, 'testfailed')
    _mozilla_central_repo_locator = (By.CSS_SELECTOR, '#th-global-navbar-top a[href*="mozilla-central"]')
    _next_ten_locator = (By.CSS_SELECTOR, 'div.btn:nth-child(1)')
    _next_twenty_locator = (By.CSS_SELECTOR, 'div.btn:nth-child(2)')
    _next_fifty_locator = (By.CSS_SELECTOR, 'div.btn:nth-child(3)')
    _notification_locator = (By.CSS_SELECTOR, 'ul#notification-box')
    _resultset_visible_locator = (By.CSS_SELECTOR, 'span.hidden.ready')
    _quick_filter_locator = (By.ID, 'quick-filter')
    _repos_menu_locator = (By.ID, 'repoLabel')
    _result_sets_locator = (By.CSS_SELECTOR, '.result-set:not(.row)')
    _unchecked_repos_links_locator = (By.CSS_SELECTOR, '#repoLabel + .dropdown-menu .dropdown-checkbox:not([checked]) + .dropdown-link')
    _unclassified_failure_count_locator = (By.ID, 'unclassified-failure-count')
    _unclassified_failure_filter_locator = (By.CSS_SELECTOR, '.btn-unclassified-failures')

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.unclassified_failure_count > 0)
        return self

    @property
    def active_watched_repo(self):
        return self.find_element(*self._active_watched_repo_locator).text

    @property
    def all_jobs(self):
        return list(itertools.chain.from_iterable([r.jobs for r in self.result_sets]))

    @property
    def checkbox_busted_is_selected(self):
        return self.find_element(*self._filter_panel_busted_failures_locator).is_selected()

    @property
    def checkbox_exception_is_selected(self):
        return self.find_element(*self._filter_panel_exception_failures_locator).is_selected()

    @property
    def checkbox_testfailed_is_selected(self):
        return self.find_element(*self._filter_panel_testfailed_failures_locator).is_selected()

    @property
    def job_details(self):
        return self.JobDetails(self)

    @property
    def notification_text(self):
        return self.find_element(*self._notification_locator).text

    @property
    def pinboard(self):
        return self.Pinboard(self)

    @property
    def result_sets(self):
        return [self.ResultSet(self, el) for el in self.find_elements(*self._result_sets_locator)]

    @property
    def results_visible(self):
        return self.find_element(*self._resultset_visible_locator)

    @property
    def unchecked_repos(self):
        return self.find_elements(*self._unchecked_repos_links_locator)

    @property
    def unclassified_failure_count(self):
        return int(self.find_element(*self._unclassified_failure_count_locator).text)

    def clear_filter(self):
        self.selenium.find_element(*self._clear_filter_locator).click()

    def click_on_filters_panel(self):
        self.find_element(*self._filter_panel_locator).click()

    def close_the_job_panel(self):
        self.find_element(*self._close_the_job_panel_locator).click()

    def deselect_all_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_all_failures_locator).click()

    def deselect_busted_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_busted_failures_locator).click()

    def deselect_exception_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_exception_failures_locator).click()

    def deselect_testfailed_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_testfailed_failures_locator).click()

    def filter_by(self, term):
        el = self.selenium.find_element(*self._quick_filter_locator)
        el.send_keys(term)
        el.send_keys(Keys.RETURN)
        self.wait.until(lambda s: self.result_sets)

    def filter_unclassified_jobs(self):
        self.find_element(*self._unclassified_failure_filter_locator).click()

    def get_next_ten_results(self):
        self.find_element(*self._next_ten_locator).click()
        self.wait.until(lambda s: len(self.result_sets) == 20)

    def get_next_twenty_results(self):
        self.find_element(*self._next_twenty_locator).click()
        self.wait.until(lambda s: len(self.result_sets) == 30)

    def get_next_fifty_results(self):
        self.find_element(*self._next_fifty_locator).click()
        self.wait.until(lambda s: len(self.result_sets) == 60)

    def open_next_unclassified_failure(self):
        el = self.find_element(*self._result_sets_locator)
        self.wait.until(EC.visibility_of(el))
        el.send_keys('n')
        self.wait.until(lambda s: self.job_details.job_result_status)

    def open_perfherder_page(self):
        self.header.switch_page_using_dropdown()

        from perfherder import PerfherderPage
        return PerfherderPage(self.selenium, self.base_url).wait_for_page_to_load()

    def open_repos_menu(self):
        self.find_element(*self._repos_menu_locator).click()

    def pin_using_spacebar(self):
        el = self.find_element(*self._result_sets_locator)
        self.wait.until(EC.visibility_of(el))
        el.send_keys(Keys.SPACE)
        self.wait.until(lambda _: self.pinboard.is_pinboard_open)

    def reset_filters(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_reset_locator).click()

    def select_mozilla_central_repo(self):
        # Fix me: https://github.com/mozilla/treeherder-tests/issues/43
        self.open_repos_menu()
        self.find_element(*self._mozilla_central_repo_locator).click()
        self.wait_for_page_to_load()

    def select_busted_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_busted_failures_locator).click()

    def select_exception_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_exception_failures_locator).click()

    def select_testfailed_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_testfailed_failures_locator).click()

    def select_random_repo(self):
        self.open_repos_menu()
        repo = random.choice(self.unchecked_repos)
        repo_name = repo.text
        repo.click()
        self.wait.until(lambda s: self._active_watched_repo_locator == repo_name)
        return repo_name

    class ResultSet(Region):

        _add_new_job_locator = (By.CSS_SELECTOR, '.open ul > li a')
        _datestamp_locator = (By.CSS_SELECTOR, '.result-set-title-left > span a')
        _dropdown_toggle_locator = (By.CLASS_NAME, 'dropdown-toggle')
        _expanded_group_content_locator = (By.CSS_SELECTOR, '.group-job-list[style="display: inline;"]')
        _group_content_locator = (By.CSS_SELECTOR, 'span.group-count-list .btn')
        _hide_runnable_jobs_locator = (By.CSS_SELECTOR, '.open ul > li:nth-child(2) > a')
        _jobs_locator = (By.CSS_SELECTOR, '.job-btn.filter-shown')
        _pin_all_jobs_locator = (By.CLASS_NAME, 'pin-all-jobs-btn')
        _platform_locator = (By.CLASS_NAME, 'platform')
        _resultset_visible_locator = (By.CSS_SELECTOR, 'span.hidden.ready')
        _runnable_jobs_locator = (By.CSS_SELECTOR, '.runnable-job-btn.filter-shown')
        _set_bottom_of_range_locator = (By.CSS_SELECTOR, '.open ul > li:nth-child(8) > a')
        _set_top_of_range_locator = (By.CSS_SELECTOR, '.open ul > li:nth-child(7) > a')

        @property
        def builds(self):
            return [self.Build(self.page, root=el) for el in self.find_elements(*self._platform_locator)]

        @property
        def datestamp(self):
            return self.find_element(*self._datestamp_locator).text

        @property
        def find_expanded_group_content(self):
            return self.is_element_displayed(*self._expanded_group_content_locator)

        @property
        def jobs(self):
            return [self.Job(self.page, root=el) for el in self.find_elements(*self._jobs_locator)]

        @property
        def results_visible(self):
            return self.find_element(*self._resultset_visible_locator)

        @property
        def runnable_jobs(self):
            return [self.Job(self.page, root=el) for el in self.find_elements(*self._runnable_jobs_locator)]

        def add_new_jobs(self):
            self.find_element(*self._dropdown_toggle_locator).click()
            self.find_element(*self._add_new_job_locator).click()
            self.wait.until(lambda s: self.is_element_displayed(*self._runnable_jobs_locator))

        def expand_group_count(self):
            self.find_element(*self._group_content_locator).click()
            self.wait.until(lambda s: self.is_element_displayed(*self._expanded_group_content_locator))

        def hide_runnable_jobs(self):
            self.find_element(*self._dropdown_toggle_locator).click()
            self.find_element(*self._hide_runnable_jobs_locator).click()
            self.wait.until(lambda s: not self.is_element_displayed(*self._runnable_jobs_locator))

        def pin_all_jobs(self):
            return self.find_element(*self._pin_all_jobs_locator).click()

        def set_as_bottom_of_range(self):
            self.find_element(*self._dropdown_toggle_locator).click()
            self.find_element(*self._set_bottom_of_range_locator).click()

        def set_as_top_of_range(self):
            self.find_element(*self._dropdown_toggle_locator).click()
            self.find_element(*self._set_top_of_range_locator).click()

        def view(self):
            return self.find_element(*self._datestamp_locator).click()

        class Build(Region):

            _platform_name_locator = (By.CSS_SELECTOR, 'td:nth-child(1) > span:nth-child(1)')

            @property
            def platform_name(self):
                return self.find_element(*self._platform_name_locator).text

        class Job(Region):

            @property
            def symbol(self):
                return self.root.text

            def click(self):
                self.root.click()
                self.wait.until(lambda _: self.page.job_details.job_result_status)

    class JobDetails(Region):

        _job_bug_locator = (By.CSS_SELECTOR, '#job-details-pane > ul > li > a > em')
        _job_details_panel_locator = (By.ID, 'job-details-panel')
        _job_result_status_locator = (By.CSS_SELECTOR, '#result-status-pane > div:nth-child(1) > span:nth-child(2)')
        _logviewer_button_locator = (By.ID, 'logviewer-btn')
        _pin_job_locator = (By.ID, 'pin-job-btn')

        @property
        def is_job_bug_visible(self):
            return self.is_element_displayed(*self._job_bug_locator)

        @property
        def job_result_status(self):
            return self.find_element(*self._job_result_status_locator).text

        def open_logviewer(self):
            self.find_element(*self._job_details_panel_locator).send_keys('l')
            window_handles = self.selenium.window_handles
            for handle in window_handles:
                self.selenium.switch_to.window(handle)
            return LogviewerPage(self.selenium, self.page.base_url).wait_for_page_to_load()

        def pin_job(self):
            el = self.find_element(*self._pin_job_locator)
            self.wait.until(EC.visibility_of(el))
            el.click()

    class Pinboard(Region):

        _root_locator = (By.ID, 'pinboard-panel')
        _add_bug_id_locator = (By.CSS_SELECTOR, '#related-bug-input')
        _add_bug_locator = (By.CSS_SELECTOR, '#pinboard-related-bugs .pinboard-preload-txt')
        _clear_all_menu_locator = (By.CSS_SELECTOR, '#pinboard-controls .dropdown-menu li:nth-child(4)')
        _jobs_locator = (By.CLASS_NAME, 'pinned-job')
        _open_save_menu_locator = (By.CSS_SELECTOR, '#pinboard-controls .save-btn-dropdown')
        _pinboard_remove_job_locator = (By.CSS_SELECTOR, '#pinned-job-list .pinned-job-close-btn')
        _save_bugs_only_menu_locator = (By.CSS_SELECTOR, '#pinboard-controls .dropdown-menu li:nth-child(2)')
        _save_pinboard_button_locator = (By.CSS_SELECTOR, '.save-btn')

        @property
        def is_pinboard_open(self):
            return self.root.is_displayed()

        @property
        def jobs(self):
            return [self.Job(self.page, el) for el in self.find_elements(*self._jobs_locator)]

        @property
        def selected_job(self):
            return next(j for j in self.jobs if j.is_selected)

        def add_bug_to_pinned_job(self, bug_id):
            self.find_element(*self._add_bug_locator).click()
            el = self.find_element(*self._add_bug_id_locator)
            el.click()
            el.send_keys(bug_id)
            el.send_keys(Keys.RETURN)

        def clear_pinboard(self):
            el = self.find_element(*self._open_save_menu_locator)
            el.click()
            self.wait.until(lambda _: el.get_attribute('aria-expanded') == 'true')
            self.find_element(*self._clear_all_menu_locator).click()

        def save_bug_to_pinboard(self):
            el = self.find_element(*self._open_save_menu_locator)
            el.click()
            self.wait.until(lambda _: el.get_attribute('aria-expanded') == 'true')
            self.find_element(*self._save_bugs_only_menu_locator).click()
            self.find_element(*self._save_pinboard_button_locator).click()

        class Job(Region):

            @property
            def is_selected(self):
                return 'selected-job' in self.root.get_attribute('class')

            @property
            def symbol(self):
                return self.root.text


class LogviewerPage(Page):

    _job_header_locator = (By.CSS_SELECTOR, 'div.job-header')

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.is_job_status_visible)
        return self

    @property
    def is_job_status_visible(self):
        return self.is_element_displayed(*self._job_header_locator)

#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


class WebView(object):

    def __init__(self, base_url, selenium, timeout=10, **kwargs):
        self.base_url = base_url
        self.timeout = timeout
        self.selenium = selenium
        self.wait = WebDriverWait(self.selenium, self.timeout)
        self.kwargs = kwargs

    @property
    def _root(self):
        return self.selenium

    def go_to_page(self):
        self.open('')

    def find_element(self, locator):
        return self._root.find_element(*locator)

    def find_elements(self, locator):
        return self._root.find_elements(*locator)

    def is_element_visible(self, locator):
        try:
            return self.selenium.find_element(*locator).is_displayed()
        except (NoSuchElementException):
            return False


class Page(WebView):

    _url = None

    def open(self):
        self.selenium.get(self.url)
        return self.wait_for_page_to_load()

    @property
    def url(self):
        if self._url is not None:
            return self._url.format(base_url=self.base_url)
        return self.base_url

    def wait_for_page_to_load(self):
        return self


class PageRegion(WebView):

    _root_locator = None

    def __init__(self, page, root=None, **kwargs):
        super(PageRegion, self).__init__(page.base_url, page.selenium, **kwargs)
        self._root_element = root
        self.page = page

    @property
    def _root(self):
        if self._root_element is None:
            if self._root_locator is not None:
                return self.selenium.find_element(*self._root_locator)
            return self.selenium
        return self._root_element

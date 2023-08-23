#!/usr/bin/python3
# -*- encoding=utf8 -*-


import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def selenium(request):
    options = Options()
    options.headless = False
    options.add_argument('--ignore-certificate-errors')
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1920, 1080)

    yield browser
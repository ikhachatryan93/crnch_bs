#! /bin/env python
import utilities
import homestars
import configparser
import json
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# from pyvirtualdisplay import Display
from get_proxies import get_new_proxies

# display = Display(visible=0, size=(1920, 1080))
# display.start()

#cb_result_urls = "https://www.crunchbase.com/app/search/companies/249a41b33de7bc8b2d2a3edcdd266278bae9c7dd"
cb_result_urls = "https://www.whatismybrowser.com/"


threads = 1
max_category_scroll_downs = 5000


def parse_config_file():
    config_parser = configparser.RawConfigParser()
    config_file = r'./configs.txt'
    config_parser.read(config_file)

    global cb_result_urls
    global max_category_scroll_downs
    global threads

    cb_result_urls = config_parser.get('search_info', 'urls')
    max_category_scroll_downs = config_parser.getint('search_info', 'max_category_scroll_downs')

    threads = config_parser.getint('parameters', 'threads')


def extract(results_url):
    browser = utilities.setup_chrome_browser(maximize=True)
    utilities.open_url(results_url, browser)
    return homestars.extract_category(browser, results_url, threads_num=threads,
                                      max_scroll_downs=max_category_scroll_downs)


def main():
    #get_new_proxies("http")
    parse_config_file()

    for url in cb_result_urls.split(","):
        data = extract(url.strip(", "))
        utilities.write_json_file(name="output.json".format(), data=data)


if __name__ == "__main__":
    main()

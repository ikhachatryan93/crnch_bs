# calling main function...
import os
import sys

from bs4 import BeautifulSoup
from selenium import webdriver

try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin

main_url_socks5 = "https://incloak.com/proxy-list/?maxtime=1500&type=5&anon=4#list"
main_url_socks4 = "https://incloak.com/proxy-list/?maxtime=1500&type=4&anon=4#list"
main_url_http = "https://incloak.com/proxy-list/?maxtime=1500&type=h&anon=4#list"
main_url_htts = "https://incloak.com/proxy-list/?maxtime=1500&type=s&anon=4#list"


# function to start browsing and getting page soup
def request(driver, proxy_type):
    if proxy_type == "http":
        driver.get(main_url_http)
    elif proxy_type == "socks5":
        driver.get(main_url_socks5)
    elif proxy_type == "socks4":
        driver.get(main_url_socks4)
    elif proxy_type == "https":
        driver.get(main_url_htts)
    else:
        raise Exception("bad proxy type")


# function to make soup
def make_soup(driver):
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    return soup


def setup_phantomjs_driver():
    driver = webdriver.PhantomJS()
    return driver


def get_new_proxies(proxy_type):
    print("Obtaining new proxies")
    driver = setup_phantomjs_driver()
    request(driver, proxy_type)
    proxy_table = driver.find_element_by_class_name("proxy__t").find_element_by_tag_name("tbody")
    proxy_lines = proxy_table.find_elements_by_tag_name("tr")

    proxies = []
    file_ = open('proxies.txt', 'w')
    for line in proxy_lines:
        objects = line.find_elements_by_tag_name("td")
        proxy = ("{}:{} \n".format(objects[0].text, objects[1].text))
        proxies.append(proxy)
        file_.write(proxy)

    driver.quit()

    return proxies

if __name__ == "__main__":
    get_new_proxies("https")

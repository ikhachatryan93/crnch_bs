from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import get_proxies
import urllib.request
import time
import json
import random
import os.path


def setup_phantomjs_browser(maximize=False):
    service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=any']
    phantomjs = webdriver.PhantomJS("phantomjs.exe", service_args=service_args)
    if maximize:
        phantomjs.maximize_window()

    return phantomjs


def get_random_line_from_file(file):
    if os.path.isfile(file):
        lines = read_urls_from_file(file)
        return random.choice(lines).strip()
    else:
        print("{} file is empty".format(file))
        return ""


def is_bad_proxy(pip):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': pip})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        req = urllib.request.Request('http://www.google.com')  # change the url address here
        sock = urllib.request.urlopen(req)
    except urllib.request.HTTPError as e:
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:
        print("ERROR:", detail)
        return True
    return False


def get_proxy(regenerate):
    if regenerate:
        get_proxies.get_new_proxies("http")
    proxy = get_random_line_from_file("proxies.txt")
    while is_bad_proxy(proxy):
        proxy = get_random_line_from_file("proxies.txt")
    return proxy


def setup_chrome_browser(maximize=True):
    pr = get_proxy(False)
    ug = get_random_line_from_file("user_agent.txt")
    print(pr)
    print(ug)
    chrome_options = Options()
    #chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--profile-directory=Default')
    #chrome_options.add_argument("load-extension=/Users/mesutgunes/Library/Application "
    #                            "Support/Google/Chrome/Default/Extensions/fdcgdnkidjaadafnichfpabhfomcebme/5.3.1_0")
    #chrome_options.add_argument("--incognito")
    #chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--user-agent=" + ug)
    chrome_options.add_argument('--proxy-server=http://%s' % pr)
    chrome = webdriver.Chrome(chrome_options=chrome_options)
    #chrome = webdriver.Chrome("chromedriver")
    if maximize:
        chrome.maximize_window()
    return chrome


# def setup_chrome_browser(maximize=True):
#    with open('proxies.txt') as f:
#        lines = f.readlines()
#        PROXY = random.choice(lines)
#    chrome_options = webdriver.ChromeOptions()
#    chrome_options.add_argument('--proxy-server=%s' % PROXY)
#    chrome = webdriver.Chrome("chromedriver", chrome_options=chrome_options)
#    if maximize:
#        chrome.maximize_window()
#    return chrome

def move_to_element(browser, element_css):
    results_grid = browser.find_elements_by_css_selector(element_css)
    action = webdriver.ActionChains(browser)
    action.move_to_element(results_grid)


def read_urls_from_file(name):
    if not os.path.isfile(name):
        return ""

    with open(name, encoding='utf-8') as f:
        urls = f.read().splitlines()

    assert (len(urls) > 0)
    return urls


def write_urls_to_file(name, urls):
    with open(name, 'w', encoding='utf-8') as f:
        for url in urls:
            try:
                f.write(url + '\n')
            except Exception as e:
                print(str(e))


def write_json_file(name, data):
    with open(name, 'w') as fname:
        json.dump(data, fname)


# return false if scrolldowns ended
def scroll_into_view(driver: webdriver, css_selector):
    return True


def open_url(url_query: str, driver: webdriver):
    driver.get(url_query)

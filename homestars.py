import threading
import sys
import time
import utilities
from bs4 import BeautifulSoup
from selenium import webdriver
from company import CrunchBaseCompanyInfo
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_companies_urls(browser, max_scroll_downs):
    cached_companies_urls_file = "cached_companies_urls.txt"
    cached_companies_urls = utilities.read_urls_from_file(cached_companies_urls_file)

    # try:
    wait = WebDriverWait(browser, timeout=5)
    number_of_results = int(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".component--results-info.cb-bold-font")))
    # except:
    #    logging.warning("Can not find number of results for {} url".format(browser.current_url))


    if number_of_results <= len(cached_companies_urls):
        print("Using already extracted urls from {} file".format(cached_companies_urls))
        return cached_companies_urls

    # start timer
    start = time.time()
    utilities.move_to_element(browser, ".component--grid")
    urls = []
    for _ in range(number_of_results / 10):
        # scroll down grid
        companies_results = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "." + CrunchBaseCompanyInfo.COMPANY_URL_CSS_CLASS)))
        utilities.scroll_into_view(browser, companies_results[10])
        # for company_result in companies_results:
        #    urls.append(company_result.get_element("href"))

    # end timer
    end = time.time()
    print("time = {}".format(end - start))
    print("Total extracted urls: {}".format(len(urls)))
    urls = list(set(urls))
    print("Deleted overlaps, total left {} urls".format(len(urls)))
    browser.quit()

    return urls


# def run_category_extraction(url, companies_infos, keyword):
#     try:
#         company = HomestarCompanyInfo(urljoin(homestars_url, url), keyword)
#         company.extract_company()
#         companies_infos.append(company.company_info)
#     except:
#         time.sleep(3)
#         try:
#             company = HomestarCompanyInfo(urljoin(homestars_url, url), keyword)
#         except Exception as e:
#             logging.error("url : {}.  {}".format(url, str(e)))


def extract_category(browser, url, threads_num, max_scroll_downs):
    print("Obtaining results from {}".format(url))
    companies_urls = get_companies_urls(browser, max_scroll_downs)
    utilities.write_urls_to_file("companies_urls.txt", companies_urls)

    done_urls_file = "done_urls.txt"
    done_urls = utilities.read_urls_from_file(done_urls_file)

    # run_category_extraction(companies_urls[0], companies_infos, keyword)
    companies_infos = []
    # trds = []
    # i = 0
    # total = len(companies_urls)
    # for url in companies_urls:
    #     i += 1
    #     sys.stdout.write("\r[Extracting: {}/{}]".format(i, total))
    #     sys.stdout.flush()
    #     time.sleep(0.3)
    #     t = threading.Thread(target=run_category_extraction, args=(url, companies_infos, keyword))
    #     t.daemon = True
    #     t.start()
    #     trds.append(t)
    #     while threading.active_count() > threads_num:
    #         time.sleep(0.4)
    # print("l2")
    # for i in trds:
    #     i.join(10)
    # print("l4")
    # logging.info("Finished. keyword: {},  companies: {}".format(keyword, len(companies_infos)))
    return companies_infos

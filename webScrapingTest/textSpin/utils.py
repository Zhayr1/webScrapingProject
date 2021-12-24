from bs4 import BeautifulSoup
import requests
from .models import KeywordsResultsReport, SingleKeywordReport
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

def get_paraphrased_text(text:str, driver:webdriver.Firefox, url:str):
    for i in range(3):
        try:
            driver.get(url)
            time.sleep(2)
            try:
                captcha_modal = driver.find_element_by_xpath('//*[@id="m2_bot_captcha"]')
                driver.execute_script("arguments[0].setAttribute('class', 'absd')", captcha_modal)
            except:
                pass    
            text_input = driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div[2]/textarea")
            text_input.send_keys(text)
            time.sleep(2)
            # driver.implicitly_wait(2)
            driver.find_element_by_xpath('//*[@id="checkButton"]').click()
            time.sleep(2)
            # driver.implicitly_wait(2)
            out_input = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div[4]/div[1]')
            result_text = out_input.get_attribute('innerText')
            return result_text
        except:
            pass 
    return None       

import time
import re

def selenium_get_paraphrased_article(object:SingleKeywordReport, url:str):
    try:
        options = Options()
        # options.headless = True
        # options.add_argument("--window-size=1920,1080")
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        print("Start spin title")
        spin_title = get_paraphrased_text(object.article_title, driver, url)
        time.sleep(3)
        print(f"Spin title: {spin_title}")
        print("end Spin Title and start spin body")
        spin_body = get_paraphrased_text(object.article_body, driver, url)
        time.sleep(3)
        # print(f"End spin body: {spin_body}")
        print(f"Old Text: {object.article_title}")
        print(f"Result Text: {spin_title}")
        if spin_title:
            object.article_title = spin_title
        if spin_body:    
            object.article_body = " ".join(str(spin_body).split())
        if spin_title or spin_body:
            object.save()
        driver.close()
        return object
    except:
        return None

def get_links(url):
    res = get_request(url)
    if res.status_code != 200:
        return None
    soup = BeautifulSoup(res.content, 'html.parser')
    results = soup.find_all('li')
    links = []
    for li in results:
        try:
            li_class = li['class']
            # li_bm = li['data-bm']
            if li_class:
                if li_class[0] == 'b_algo':
                    # print(li)
                    # print(li.h2.a.get('href'))
                    links.append(li.a.get('href'))
        except Exception as e:
            pass
    return links    

def validate_links(links, spinLinks):
    difference = list(set(links) - set(spinLinks))
    if difference:
        return difference
    else:
        return None    

def get_article_from_keyword(keyword:str, keyword_result_report:KeywordsResultsReport):
    try:
        with open('spin.txt') as f:
            lines = f.readlines()
        if lines:    
            lines = lines[0].split(',')
            print(f"Lines: {lines}")
    except:
        lines = []
    query = keyword.replace(' ','+')
    pageCounter = 1
    val_links = []
    for i in range(1000):
        url = f"https://www.bing.com/search?q={query}+site%3Awordpress.com&first={pageCounter}"
        links = get_links(url)
        if not links:
            return None
        val = validate_links(links, lines)
        if val:
            val_links = val
            break
        else:
            pageCounter += 10
    skr = SingleKeywordReport(report=keyword_result_report,keyword="", article_title="", article_body="")
    for link in val_links:
        res = get_title_and_body_from_url(link, keyword, skr)
        seoToolUrl = "https://seotoolscentre.com/paraphrase-tool"
        res = selenium_get_paraphrased_article(res, seoToolUrl)
        if res:
            file_was_created = res.create_article_file()
            return file_was_created
    return None        


def get_title_and_body_from_url(url:str, keyword:str, single_report:SingleKeywordReport):
    res = get_request(url)
    if res.status_code != 200:
        return None
    soup = BeautifulSoup(res.content, 'html.parser')
    title = soup.title.string
    body = soup.get_text().strip()
    # print(soup.body)
    single_report.keyword = keyword
    single_report.article_title = title
    single_report.article_body = body
    single_report.save()
    # skr = SingleKeywordReport(keyword=keyword, article_title=title, article_body=body)
    # print(skr.article_title)
    f = open("spin.txt", "a")
    f.write(f"{url},")
    f.close()
    return single_report

def get_request(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    return requests.get(url, headers=headers)

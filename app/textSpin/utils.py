from bs4 import BeautifulSoup
import requests
from .models import KeywordsResultsReport, SingleKeywordReport
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from urllib.parse import urlparse 

def send_message(channel_name:str, type:str, payload_type, payload:dict):
    channel_layer = get_channel_layer()
    payload['type'] = payload_type
    async_to_sync(channel_layer.group_send)(channel_name, {
            'type': f'{type}',
            'payload': payload
    })

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

def selenium_get_paraphrased_article(object:SingleKeywordReport, url:str):
    try:
        options = Options()
        options.headless = True
        # # options.add_argument("--window-size=1920,1080")
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        spin_title = get_paraphrased_text(object.article_title, driver, url)
        time.sleep(3)
        spin_body = get_paraphrased_text(object.article_body, driver, url)
        time.sleep(3)
        # print(f"Old Text: {object.article_title}")
        # print(f"Result Text: {spin_title}")
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
    val_links = []
    flag = False
    for link in links:
        for spinLink in spinLinks:
            if spinLink:
                # print(f"spinLink: {spinLink} is in: {link}: {spinLink in link}")
                if spinLink in link:
                    print(f"{spinLink} in {link} = {spinLink in link}")
                    flag = True
        if not flag:
            val_links.append(link)
            flag = False
    return val_links

def get_article_from_keyword(keyword:str, keyword_result_report:KeywordsResultsReport):
    try:
        with open('spin.txt') as f:
            lines = f.readlines()
        if lines:    
            lines = lines[0].split(',')
            # print(f"Lines: {lines}")
    except:
        lines = []
    query = keyword.replace(' ','+')
    pageCounter = 1
    val_links = []
    print("start to get and validate links")
    for i in range(1000):
        print(f'for iterations por links {i}')
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
    # options = Options()
    # options.headless = True
    # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    print("start selenium part")
    for link in val_links:
        res = get_title_and_body_from_url(link, keyword, skr)
        seoToolUrl = "https://seotoolscentre.com/paraphrase-tool"
        res = selenium_get_paraphrased_article(res, seoToolUrl)
        if res:
            file_was_created = res.create_article_file()
            if file_was_created:
                send_message('test1234', 'send.message', 'article_spun', { "article_spun": True })
            return file_was_created
    return None        

from bs4.element import Comment

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def get_article_images(url):
    res = get_request(url)
    div_id = "mmComponent_images_2"
    if res.status_code != 200:
        return None
    soup = BeautifulSoup(res.content, 'html.parser')
    imgs = soup.find_all('img')
    for img in imgs:
        print(img)
    pass


def get_root_domain(url):
    parsed_uri = urlparse(url) 
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    result = domain.replace('www.', '')  # as per your case
    return result

def get_title_and_body_from_url(url:str, keyword:str, single_report:SingleKeywordReport):
    res = get_request(url)
    if res.status_code != 200:
        return None
    soup = BeautifulSoup(res.content, 'html.parser')
    title = soup.title.string
    body = text_from_html(res.content)
    # print(soup.body)
    single_report.keyword = keyword
    single_report.article_title = title
    single_report.article_body = body
    single_report.save()
    # skr = SingleKeywordReport(keyword=keyword, article_title=title, article_body=body)
    # print(skr.article_title)
    f = open("spin.txt", "a")
    f.write(f"{get_root_domain(url)},")
    f.close()
    return single_report

def get_request(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    return requests.get(url, headers=headers, timeout=5)

from datetime import date, datetime

def get_and_save_images(keyword:str, articles_number:int):
    keyword = keyword.replace(' ','+')
    url = f"https://www.bing.com/images/search?tsc=ImageBasicHover&q={keyword}+site%3awordpress.com&qft=+filterui:imagesize-large&form=IRFLTR&first=1"
    img_urls = get_article_images(url, articles_number*3)

    path = f"media/articles/{keyword.replace('+', '_')}"
    try:
        os.mkdir(path)
    except:
        pass
    if img_urls:
        for i in range(len(img_urls)):
            url = img_urls[i]
            img_name = keyword.replace('+','_')
            img_format = get_format(url)

            fetch_image(url, f"media/articles/{img_name}/{datetime.now()}_{img_name}.{img_format}")

import os
def get_article_images(url, n_images):
    res = get_request(url)
    if res.status_code != 200:
        return None
    soup = BeautifulSoup(res.content, 'html.parser')
    imgs = soup.find_all()
    murls = []
    for img in imgs:
        if img.get('m'):
            mdata = json.loads(img.get('m'))
            if len(murls) < n_images:
                murls.append(mdata['murl'])
    return murls            

import requests
from io import open as iopen
 
def fetch_image(img_ur, save_filename):
    img = requests.get(img_ur)
    if img.status_code == 200:
        with iopen(save_filename, 'wb') as f:
            f.write(img.content)
    else:
        print('Received error: {}'.format(img.status_code))
 

def get_format(url:str) -> str:
    if url.count('.jpg') > 0:
        return 'jpg'
    elif url.count('.png') > 0:
        return 'png'
    else:
        return 'jpg'
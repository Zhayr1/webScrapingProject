from bs4 import BeautifulSoup
import requests
import json

def get_request(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
    }
    return requests.get(url, headers=headers)

def get_article_images(url, n_images):
    res = get_request(url)
    div_id = "mmComponent_images_2"
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

if __name__ == "__main__":
    keyword = "Eco friendly products"
    keyword = keyword.replace(' ','+')
    url = f"https://www.bing.com/images/search?tsc=ImageBasicHover&q={keyword}+site%3awordpress.com&qft=+filterui:imagesize-large&form=IRFLTR&first=1"
    img_urls = get_article_images(url, 3)
    if img_urls:
        for i in range(len(img_urls)):
            url = img_urls[i]
            img_name = keyword.replace('+','_')
            img_format = get_format(url)

            fetch_image(url, f"media/articles/{img_name}/{i}_{img_name}.{img_format}")

    # testlink = 'https://vignette.wikia.nocookie.net/pdsh/images/9/95/Prettygoldilocks.jpg'
    # filename = 'Goldilocks.jpg'
    # fetch_image(testlink, filename)            
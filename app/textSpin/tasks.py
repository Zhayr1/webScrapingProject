from celery import shared_task

from .utils import get_article_from_keyword
from .models import KeywordsResultsReport, SingleKeywordReport
from .utils import send_message

@shared_task()
def process_scraping_request_task(post_data):
    if post_data:
        # keywords = str(file.read().decode('UTF-8'))
        # keywords = keywords.splitlines()
        keywords = post_data['keywords']
        articles_number = post_data['articles_number']
        # send_message('test1234', 'send.message', 'total_keywords',{ "total_keywords": len(keywords) })
        n_keywords = len(keywords) * articles_number
        krp = KeywordsResultsReport(keywords=keywords, number_of_articles=articles_number, number_of_keywords=n_keywords)
        # krp.set_number_of_articles()
        krp.save()
        for kw in keywords:
            print(f"kw: {kw}")
            # try:
            #     get_and_save_images(kw, articles_number)
            # except:
            #     print('error while fetching images')    
            for i in range(articles_number):
                res = start_scraping_task(kw, krp.id)
                # if res:
                    # send_message('test1234', 'send.message', { "keyword_processed": True })
                # print(res)
            send_message('test1234', 'send.message', 'keyword_processed', { "keyword_processed": True })
        send_message('test1234', 'send.message', 'task_finished', {'task_finished': True })

@shared_task(bind=True)
def start_scraping_task(self, keyword:str, krp_id:int):
    print("start scraping task init")
    try:
        krp = KeywordsResultsReport.objects.get(id=krp_id)
    except:
        print('krp not found')    
        return None
    res = get_article_from_keyword(keyword, krp)
    print(f"Task Result: {res}")
    # if res:
        # send_message('test1234', 'send.message', 'keyword_processed', { "keyword_processed": True })
    return res

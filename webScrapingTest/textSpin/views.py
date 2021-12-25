from django.shortcuts import render
from .models import KeywordsResultsReport
from .tasks import start_scraping_task, process_scraping_request_task
from .utils import send_message


def articleScrapingView(request):
    template_name = "articleScrapingView.html"
    if request.POST:
        try:
            file = request.FILES['keywords_file']
            keywords = str(file.read().decode('UTF-8'))
            keywords = keywords.splitlines()
        except Exception as e:
            print(f"ex: {e}")
            return render(request, template_name, {'error':'you must attach a keyword_file.txt'})
        try:    
            articles_number = int(request.POST['articles_number'])
        except:
            return render(request, template_name, {'error':"articles number can't be empty"})    
        # print(f"Task test: {add.delay(2,3)}")
        post_data = {
            "keywords": keywords,
            "articles_number": articles_number
        }
        process_scraping_request_task.delay(post_data)
        return render(request, template_name, {
            'success':'True',
            'total_keywords': len(keywords),
            'articles_per_keyword': articles_number
        })

    return render(request, template_name, {})
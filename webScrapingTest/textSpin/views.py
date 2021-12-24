from django.shortcuts import render
from .utils import get_article_from_keyword
from .models import KeywordsResultsReport

# Create your views here.
def articleScrapingView(request):
    template_name = "articleScrapingView.html"
    if request.POST:
        # print(f"Request POST {request.POST}")
        # print(f"Request Files {request.FILES}")
        file = request.FILES['keywords_file']
        articles_number = int(request.POST['articles_number'])  
        keywords = str(file.read().decode('UTF-8'))
        keywords = keywords.splitlines()
        krp = KeywordsResultsReport(keywords=keywords, number_of_articles=articles_number)
        krp.save()
        for kw in keywords:
            print(f"kw: {kw}")
            for i in range(articles_number):
                res = get_article_from_keyword(kw, krp)
                print(res)
        return render(request, template_name, {'success':'True'})
    else:    
        return render(request, template_name, {})
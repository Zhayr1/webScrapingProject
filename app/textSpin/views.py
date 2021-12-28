from django.shortcuts import render
from .models import KeywordsResultsReport, SingleKeywordReport, ArticleImages
from .tasks import process_scraping_request_task
from django.views.generic import ListView

from django.http import Http404, HttpResponse
import os
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

def request_download(request, pk):
    try:
        print(f"pk: {pk}")
        req = SingleKeywordReport.objects.get(pk=pk)
        file_path = f"media/articles/{req.keyword.replace(' ','_')}/{req.id}_{req.keyword.replace(' ','_')}.txt"
        # file_path = os.path.join(settings.MEDIA_ROOT, fname)
        print(f"File Path: {file_path}")
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    except Exception as e:
        print(f"Ex: {e}")
        raise Http404

import shutil

def request_image_download(request, pk, img_index):
    try:
        req = ArticleImages.objects.get(pk=pk)
        path = req.get_image_path(img_index)
        if not path:
            print(f"Fail Path: {path}")
            return Http404
        with open(path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(path)
            fh.close()    
            return response
        pass
    except Exception as e:
        print(f"Ex: {e}")
        return Http404
        pass
    pass

def request_zip_download(request, pk, keyword):
    try:
        keyword = keyword.replace('_',' ')
        req = SingleKeywordReport.objects.filter(report__id=pk, keyword=keyword)
        if req:
            req = req[0]
        else:
            raise Exception("Request not found")    
        file_path = f"media/articles/{req.keyword.replace(' ','_')}"
        print(f"File Path: {file_path}")
        zip_files_path = 'media/articles/zip'
        try:
            os.mkdir(zip_files_path)
        except:
            pass
        created = shutil.make_archive(f"{zip_files_path}/{req.keyword.replace(' ','_')}", 'zip', file_path)
        zip_path = zip_files_path + f'/{req.keyword.replace(" ","_")}.zip'
        with open(zip_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/zip")
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(file_path)
            return response
    except Exception as e:
        print(f"Ex: {e}")
        raise Http404

class ReportDeleteView(DeleteView):
    model = KeywordsResultsReport
    success_url = reverse_lazy('textSpin:list')
    template_name = "keywordResultReport_confirm_delete.html"

class SingleReportLinkList(ListView):
    template_name = 'linksList.html'
    # model = KeywordsResultsReport
    model = SingleKeywordReport
    
    def get_queryset(self):
        return self.model.objects.filter(report__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skr_id'] = self.kwargs['pk']
        keywords = []
        images = []
        res = SingleKeywordReport.objects.filter(report__id=self.kwargs['pk'])
        for skr in res:
            keywords.append(skr.keyword.replace(' ','_'))
            try:
                images.append(ArticleImages.objects.get(article=skr))
            except:
                pass    
        keywords = list(set(keywords))
        context['keywords'] = keywords
        context['images_list'] = images
        # context['images_list'] = 
        return context    

class KeywordResultsView(ListView):
    template_name = "resultsListView.html"
    model = KeywordsResultsReport
    queryset = KeywordsResultsReport.objects.all().order_by('-id')


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


from django.urls import path
from .views import articleScrapingView, KeywordResultsView, SingleReportLinkList,ReportDeleteView, request_download

app_name = 'textSpin'

urlpatterns = [
    path('scraping/', articleScrapingView, name='index'),
    path('list/', KeywordResultsView.as_view(), name='list'),
    path('list/delete/<pk>/', ReportDeleteView.as_view(), name='delete'),
    path('list/download/list/<pk>/', SingleReportLinkList.as_view(), name='download_list'),
    path('list/download/file/<pk>/', request_download, name='download_file')
]
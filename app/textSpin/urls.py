from django.urls import path
from .views import articleScrapingView, KeywordResultsView, SingleReportLinkList,ReportDeleteView, request_download, request_zip_download, request_image_download


app_name = 'textSpin'

urlpatterns = [
    path('scraping/', articleScrapingView, name='index'),
    path('list/', KeywordResultsView.as_view(), name='list'),
    path('list/delete/<pk>/', ReportDeleteView.as_view(), name='delete'),
    path('list/download/list/<pk>/', SingleReportLinkList.as_view(), name='download_list'),
    path('list/download/file/<pk>/', request_download, name='download_file'),
    path('list/download/zip/<pk>/<str:keyword>/', request_zip_download, name='download_zip'),
    path('list/download/image/<pk>/<int:img_index>/', request_image_download, name='download_image')
]
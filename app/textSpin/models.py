from django.db import models
import os

# Create your models here.
class KeywordsResultsReport(models.Model):
    keywords = models.TextField()
    number_of_articles = models.IntegerField()
    number_of_keywords = models.IntegerField(default=0)
    date = models.DateField(auto_now=True)


class SingleKeywordReport(models.Model):
    report = models.ForeignKey(KeywordsResultsReport, on_delete=models.CASCADE, null=True)
    keyword = models.CharField(max_length=256)
    article_title = models.TextField(null=True)
    article_body = models.TextField(null=True)
    article_url = models.CharField(max_length=2048, default=0, null=True)

    def __str__(self) -> str:
        return f"SingleKeywordReport: {self.keyword}"

    def create_article_file(self, directory="media/articles/") -> bool:
        try:
            path = f"{directory}{self.keyword.replace(' ', '_')}"
            try:
                os.mkdir(path)
            except:
                pass    
            print(f"Path: {path}")
            print(f"FilePath: {path}/{self.keyword.replace(' ','_')}")
            filepath = f"{path}/{self.id}_{self.keyword.replace(' ','_')}.txt"
            f = open(filepath, "a")
            f.write(f"{self.article_title}\n\n\n{self.article_body}")
            f.close()
            self.article_url = filepath
            self.save()
            return True
        except:
            return False

class ArticleImages(models.Model):
    article = models.ForeignKey(SingleKeywordReport, on_delete=models.CASCADE)
    url_image_1 = models.CharField(max_length=1024, default="")
    url_image_2 = models.CharField(max_length=1024, default="")
    url_image_3 = models.CharField(max_length=1024, default="")

    path_image_1 = models.CharField(max_length=1024, default="")
    path_image_2 = models.CharField(max_length=1024, default="")
    path_image_3 = models.CharField(max_length=1024, default="")

    def get_images_urls(self) -> list:
        return [ self.url_image_1, self.url_image_2, self.url_image_3 ]

    def set_image_url(self, index:int, url:str):
        if index == 1:
            self.url_image_1 = url
        elif index == 2:
            self.url_image_2 = url
        elif index == 3:
            self.url_image_3 = url  

    def set_image_path(self, index:int, path:str):
        if index == 1:
            self.path_image_1 = path
        elif index == 2:
            self.path_image_2 = path
        elif index == 3:
            self.path_image_3 = path

    def get_image_path(self, index):
        if index == 1:
            return self.path_image_1
        elif index == 2:
            return self.path_image_2
        elif index == 3:
            return self.path_image_3
        return None    
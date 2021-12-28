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
    image_1 = models.CharField(max_length=1024)
    image_2 = models.CharField(max_length=1024)
    image_3 = models.CharField(max_length=1024)

    def get_images_urls(self) -> list:
        return [ self.image_1, self.image_2, self.image_3 ]
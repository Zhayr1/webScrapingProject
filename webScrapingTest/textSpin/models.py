from django.db import models
import os

# Create your models here.
class KeywordsResultsReport(models.Model):
    keywords = models.TextField()
    number_of_articles = models.IntegerField()
    date = models.DateField(auto_now=True)

class SingleKeywordReport(models.Model):
    report = models.ForeignKey(KeywordsResultsReport, on_delete=models.CASCADE, null=True)
    keyword = models.CharField(max_length=256)
    article_title = models.TextField(null=True)
    article_body = models.TextField(null=True)

    def __str__(self) -> str:
        return f"SingleKeywordReport: {self.keyword}"

    def create_article_file(self, directory="media/articles/") -> bool:
        
        try:
            path = f"{directory}{self.keyword.replace(' ', '_')}"
            os.mkdir(path)
            print(f"Path: {path}")
            print(f"FilePath: {path}/{self.keyword.replace(' ','_')}")
            f = open(f"{path}/{self.keyword.replace(' ','_')}.txt", "a")
            f.write(f"{self.article_title}\n\n\n{self.article_body}")
            f.close()
            return True
        except:
            return False

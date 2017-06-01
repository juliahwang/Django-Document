import datetime
from django.db import models

# Create your models here.
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # <choice>_set은 어디서 생겨나나?
    # ForeignKey를 사용하여 다른 모델의 pk값을 불러올 때 자동을 생성되어 쿼리셋에서 사용할 수 있다.
    # <>안은 변경가능.
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField() #글자수 제한 X
    created_at = models.DateTimeField()
    def __str__(self): #object 이름을 table로 반환하도록 str 함수를 오버라이딩
        return f'{[self.pk]} {self.title}'

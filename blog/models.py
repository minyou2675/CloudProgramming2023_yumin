import os.path

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField() #글자수 제한 X

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/',blank=True) #blank -> 필수항목 아님, upload to 경로에 이미지 저장
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d',blank=True)

    created_at = models.DateTimeField(auto_now_add=True) # 컬럼에 추가될 때 생김
    updated_at = models.DateTimeField(auto_now=True) # 자동추가
    
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE) #CASCADE()XXX 지워지게 되면 그 함수를 실행하라 CALL-BACK

    def __str__(self): #object 이름을 table로 반환하도록 str 함수를 오버라이딩
        return f'{[self.pk]} {self.title} - {self.author}'
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

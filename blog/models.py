import os.path

from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
from markdownx.models import MarkdownxField

class Tag(models.Model):
  name = models.CharField(max_length=20, unique=True) #unique=True 다른 레코드의 name 필드와 겹치면 생성안된다
  slug = models.SlugField(max_length=50, unique=True, allow_unicode=True) #allow_unicode -> slugField만 있는 파라미터 --> 영어외에도 접근 가능
  
  def __str__(self):
        return self.name 
  def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'   

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True) #unique=True 다른 레코드의 name 필드와 겹치면 생성안된다
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True) #allow_unicode -> slugField만 있는 파라미터 --> 영어외에도 접근 가능

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'
    class Meta:
        verbose_name_plural = 'Categories' #복수형 이름 수정

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = MarkdownxField() #글자수 제한 X

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/',blank=True) #blank -> 필수항목 아님, upload to 경로에 이미지 저장
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d',blank=True)

    created_at = models.DateTimeField(auto_now_add=True) # 컬럼에 추가될 때 생김
    updated_at = models.DateTimeField(auto_now=True) # 자동추가
    
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE) #CASCADE()XXX 지워지게 되면 그 함수를 실행하라 CALL-BACK
    category = models.ForeignKey(Category,null=True, on_delete=models.SET_NULL,default=1) #카테고리가 없어지면 Post의 카테고리는 null로 default는??

    tag = models.ManyToManyField(Tag,null=True) #Null은 서버사이드 validation(DB 입력 기준) blank는 view에서 validation

    def __str__(self): #object 이름을 table로 반환하도록 str 함수를 오버라이딩
        return f'{[self.pk]} {self.title} - {self.author}'
    
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_content_markdown(self):
        return markdown(self.content) #컨텐트를 마크다운으로 변환해서 return

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) # 컬럼에 추가될 때 생김
    updated_at = models.DateTimeField(auto_now=True) # 자동추가

    def __str__(self):
        return f'{self.author} - {self.content}'
    
    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
    

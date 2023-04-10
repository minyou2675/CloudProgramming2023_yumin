from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post,Category, Tag 


# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-pk'  # 내림차순
    
    def get_context_data(self,**kwargs): #오버라이딩
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post

def categories_page(request, slug):
    if slug == 'no-category':
        category='미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    context = {
        'category' : category, 
        'categories' : Category.objects.all(),
        'post_list' : post_list,
        'no_category_count' : Post.objects.filter(category=None).count()
    }
    return render(request,  'blog/post_list.html',context)

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all() #tag를 참조하고 있는 포스트들을 다 가져와라 
    context = {
        'tag' : tag, 
        'categories' : Category.objects.all(),
        'post_list' : post_list,
        'no_category_count' : Post.objects.filter(category=None).count()
    }
    return render(request,'blog/post_list.html',context)
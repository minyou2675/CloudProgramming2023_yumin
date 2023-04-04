from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post,Category


# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-pk'  # 내림차순
    
    def get_context_data(self,**kwargs): #오버라이딩
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post

def categories_page(request, slug):
    category = Category.objects.get(slug=slug)
    context = {
        'category' : category, 
        'categories' : Category.objects.all(),
        'post_list' : Post.objects.filter(category=category), 
    }
    return render(request, context, 'post_list.html')
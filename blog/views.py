from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import Post,Category, Tag 


# Create your views here.

class PostUpdate(LoginRequiredMixin, UpdateView):
     model = Post
     fields = ['title','content','head_image','file_upload','category','tag']
     template_name = 'blog/post_update.html'
     def dispatch(self, request ,*args,**kwargs):
         if request.user.is_authenticated and self.get_object().author == request.user: #로그인한 사용자와 글의 author가 일치할 시
             return super(PostUpdate,self).dispatch(request, *args, **kwargs) #PostUpdate에 정의되어 있는 본래 Dispatch를 그대로 실행
         else:
             raise PermissionError
     

class PostCreate(LoginRequiredMixin,CreateView):
    model = Post #PostCreate에 접근 시 post라는 하나의 인스턴스를 만들겠다.
    fields = ['title','content','head_image','file_upload','category','tag'] # 이 7개의 값을 입력받도록 한다.
    
    def test_function(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    
    def form_valid(self, form): #PostCreate에서 form의 POST 메소드를 보냈을 때 실행
        current_user = self.request.user #유저 정보를 가져옴. django의 request는 항상 사용자 항목을 가지고 있다. 
        if current_user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser): #로그인이 된 상태에서, user가 staff거나 superuser여야만 한다.
            form.instance.author = current_user #현재 form에는 author 필드가 없는데, 필드를 생성하고 거기에 user를 집어넣는다.
            return super(PostCreate, self).form_valid(form)
        else:
            redirect('/blog/')
    
    

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
    
    def get_context_data(self,**kwargs): #오버라이딩
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context

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

def add_comment(request, pk): #폼을 통해 post를 보내는 경우 and url을 입력하여 get으로 호출하는 경우
    if not request.user.is_authenticated:
        raise PermissionError
    if request.method =='POST':
        post = Post.objects.get(pk = pk)
        comment_form = CommentForm(request.POST) #POST안에 들어있는 method body
        comment_temp = comment_form.save(commit=False) #DB에 보내지 않고 COMMENT 개체를 생성
        comment_temp.post = post
        comment_temp.author = request.user
        comment_temp.save() #바로 DB로 전송
        
        return redirect(post.get_absolute_url())
    
 

    else:
        raise PermissionError
    


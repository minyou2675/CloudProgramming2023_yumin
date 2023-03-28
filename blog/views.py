from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Post


# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-pk'  # 내림차순


class PostDetail(DetailView):
    model = Post

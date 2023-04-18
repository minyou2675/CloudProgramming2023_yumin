from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view()), #as_view -> generic이 view로 구현하는 메쏘드
    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>/', views.categories_page),
    path('tag/<str:slug>/', views.tag_page),
    path('create_post/', views.PostCreate.as_view()),# view로 만들어 주십쇼 
    path('update_post/<int:pk>', views.PostUpdate.as_view()),
    path('<int:pk>/add_comment/', views.add_comment),
]

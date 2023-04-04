from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view()), #as_view -> generic이 view로 구현하는 메쏘드
    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>/', views.categories_page)
]

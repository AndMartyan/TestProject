from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import RegisterView
from .models import Post

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('posts/', views.PostView.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('register/', RegisterView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)


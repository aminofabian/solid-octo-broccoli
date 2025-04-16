from django.urls import path
from . import views

urlpatterns = [
    # HTML Views
    path('', views.blog_list, name='blog-list'),  # List all blogs (HTML view)
    path('<int:pk>/', views.blog_detail, name='blog-detail'),  # Detail view for a specific blog
    
    # API Endpoints
    path('api/blogs/', views.get_blogs, name='api-blog-list'),
    path('api/blogs/create/', views.create_blog, name='api-blog-create'),
    path('api/blogs/<int:pk>/', views.blog_detail, name='api-blog-detail'),
]


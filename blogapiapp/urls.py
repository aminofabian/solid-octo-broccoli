from django.urls import path
from . import views

urlpatterns = [
    # HTML Views
    path('', views.blog_list, name='blog-list'),  # List all blogs (HTML view)
    path('<int:pk>/', views.blog_detail, name='blog-detail'),  # Detail view for a specific blog
    
    # API Endpoints
    path('api/', views.index, name='index'),  # API index endpoint
    path('api/blogs/', views.get_blogs, name='get-blogs'),  # API endpoint for blogs
    path('api/blogs/<int:pk>/', views.get_blog_detail, name='get-blog-detail'),
    path('api/blogs/create/', views.create_blog, name='create-blog'),
    path('api/blogs/<int:pk>/update/', views.update_blog, name='update-blog'),
    path('api/blogs/<int:pk>/delete/', views.delete_blog, name='delete-blog'),
]


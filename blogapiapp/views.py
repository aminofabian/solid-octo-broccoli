from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Blog
from .serializers import BlogSerializer, BlogCreateSerializer, BlogUpdateSerializer

@swagger_auto_schema(
    method='get',
    operation_description="Returns a hello world message",
    responses={200: openapi.Response(
        description="Successful response",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING)
            }
        )
    )}
)
@api_view(['GET'])
def index(request):
    """
    A simple view that returns a hello world message
    """
    return Response({'message': 'Hello, World!'})   


@api_view(['GET'])
def get_blogs(request):
    """
    A simple view that returns all blogs
    """
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blogapiapp/blog_list.html', {'blogs': blogs})

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blogapiapp/blog_detail.html', {'blog': blog})

@swagger_auto_schema(
    method='get',
    operation_description="Retrieve a specific blog post by ID",
    responses={
        200: BlogSerializer,
        404: openapi.Response(
            description="Blog not found",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    }
)
@api_view(['GET'])
def get_blog_detail(request, pk):
    """
    Retrieve a blog post by its ID
    """
    try:
        blog = Blog.objects.get(pk=pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    except Blog.DoesNotExist:
        return Response(
            {"error": "Blog not found"}, 
            status=404
        )


@swagger_auto_schema(
    method='post',
    request_body=BlogCreateSerializer,
    responses={
        201: BlogSerializer,
        400: openapi.Response(
            description="Bad Request",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING)
                }
            )
        )
    }
)
@api_view(['POST'])
def create_blog(request):
    """
    Create a new blog post
    """
    serializer = BlogCreateSerializer(data=request.data)
    if serializer.is_valid():
        blog = serializer.save()
        response_serializer = BlogSerializer(blog)
        return Response(response_serializer.data, status=201)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(
    method='put',
    request_body=BlogUpdateSerializer,
    responses={
        200: BlogSerializer,
        404: openapi.Response(description="Blog not found")
    }
)
@api_view(['PUT'])
def update_blog(request, pk):
    """
    Update a blog post
    """
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=404)

    serializer = BlogUpdateSerializer(blog, data=request.data)
    if serializer.is_valid():
        blog = serializer.save()
        response_serializer = BlogSerializer(blog)
        return Response(response_serializer.data)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(
    method='delete',
    responses={
        204: openapi.Response(description="Blog deleted successfully"),
        404: openapi.Response(description="Blog not found")
    }
)
@api_view(['DELETE'])
def delete_blog(request, pk):
    """
    Delete a blog post
    """
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=404)
    
    blog.delete()
    return Response(status=204)


from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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


@swagger_auto_schema(
    method='get',
    operation_description="List all blog posts with optional filtering",
    manual_parameters=[
        openapi.Parameter('search', openapi.IN_QUERY, description="Search in title and content", type=openapi.TYPE_STRING),
        openapi.Parameter('sort', openapi.IN_QUERY, description="Sort by field (created_at, -created_at, title, -title)", type=openapi.TYPE_STRING),
    ],
    responses={200: BlogSerializer(many=True)}
)
@api_view(['GET'])
def get_blogs(request):
    """
    List all blogs with optional search and sorting
    """
    queryset = Blog.objects.all()
    
    # Search functionality
    search_query = request.query_params.get('search', '')
    if search_query:
        queryset = queryset.filter(title__icontains=search_query) | queryset.filter(content__icontains=search_query)
    
    # Sorting
    sort_by = request.query_params.get('sort', '-created_at')
    if sort_by in ['created_at', '-created_at', 'title', '-title']:
        queryset = queryset.order_by(sort_by)
    
    serializer = BlogSerializer(queryset, many=True)
    return Response({
        'count': queryset.count(),
        'results': serializer.data
    })

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blogapiapp/blog_list.html', {'blogs': blogs})

@swagger_auto_schema(
    methods=['get', 'put', 'delete'],
    operation_description="Retrieve, update or delete a blog post",
    request_body=BlogUpdateSerializer,
    responses={
        200: BlogSerializer,
        404: openapi.Response(
            description="Blog not found",
            examples={"application/json": {"error": "Blog not found"}}
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={"application/json": {"title": ["This field is required."]}}
        )
    }
)
@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request, pk):
    """
    Retrieve, update or delete a blog post
    """
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BlogUpdateSerializer(blog, data=request.data)
        if serializer.is_valid():
            blog = serializer.save()
            response_serializer = BlogSerializer(blog)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(
    method='post',
    request_body=BlogCreateSerializer,
    responses={
        201: BlogSerializer,
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "title": ["This field is required."],
                    "content": ["This field is required."]
                }
            }
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
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    return Response(status=status.HTTP_204_NO_CONTENT)


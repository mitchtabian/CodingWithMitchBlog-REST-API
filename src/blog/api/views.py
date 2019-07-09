from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from account.models import Account
from blog.models import BlogPost
from blog.api.serializers import BlogPostSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def api_detail_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = BlogPostSerializer(blog_post)
		return Response(serializer.data)


@api_view(['PUT',])
@permission_classes((IsAuthenticated, ))
def api_update_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if blog_post.author != user:
		return Response({'response':"You don't have permission to edit that."}) 
		
	if request.method == 'PUT':
		serializer = BlogPostSerializer(blog_post, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = UPDATE_SUCCESS
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE',])
@permission_classes((IsAuthenticated, ))
def api_delete_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if blog_post.author != user:
		return Response({'response':"You don't have permission to delete that."}) 

	if request.method == 'DELETE':
		operation = blog_post.delete()
		data = {}
		if operation:
			data['response'] = DELETE_SUCCESS
		return Response(data=data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def api_create_blog_view(request):

	blog_post = BlogPost(author=request.user)

	if request.method == 'POST':
		serializer = BlogPostSerializer(blog_post, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET',])
@permission_classes((IsAuthenticated, ))
def api_blog_list_view(request):

	blog_posts = BlogPost.objects.all()




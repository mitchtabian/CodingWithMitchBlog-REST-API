from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from account.models import Account
from blog.models import BlogPost
from blog.api.serializers import BlogPostSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'

# Response: https://gist.github.com/mitchtabian/93f287bd1370e7a1ad3c9588b0b22e3d
# Url: https://<your-domain>/api/blog/<slug>/
# Headers: Authorization: Token <token>
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


# Response: https://gist.github.com/mitchtabian/32507e93c530aa5949bc08d795ba66df
# Url: https://<your-domain>/api/blog/<slug>/update
# Headers: Authorization: Token <token>
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


# Response: https://gist.github.com/mitchtabian/a97be3f8b71c75d588e23b414898ae5c
# Url: https://<your-domain>/api/blog/<slug>/delete
# Headers: Authorization: Token <token>
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


# Response: https://gist.github.com/mitchtabian/78d7dcbeab4135c055ff6422238a31f9
# Url: https://<your-domain>/api/blog/create
# Headers: Authorization: Token <token>
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


# Response: https://gist.github.com/mitchtabian/ae03573737067c9269701ea662460205
# Url: 
#		1) list: https://<your-domain>/api/blog/list
#		2) pagination: http://<your-domain>/api/blog/list?page=2
#		3) search: http://<your-domain>/api/blog/list?search=mitch
#		4) ordering: http://<your-domain>/api/blog/list?ordering=-date_updated
#		4) search + pagination + ordering: <your-domain>/api/blog/list?search=mitch&page=2&ordering=-date_updated
# Headers: Authorization: Token <token>
class ApiBlogListView(ListAPIView):
	queryset = BlogPost.objects.all()
	serializer_class = BlogPostSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('title', 'body', 'author__username')
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from blog.models import BlogPost
from blog.serializers import BlogPostSerializer

from django.views.decorators.csrf import csrf_exempt


@api_view(['GET',])
def api_detail_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = BlogPostSerializer(blog_post)
		print(serializer.data)
		return Response(serializer.data)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from blog.models import BlogPost
from blog.serializers import BlogPostSerializer


@api_view(['GET',])
def api_detail_blog_view(request, slug):

	try:
		blog_post = BlogPost.objects.get(slug=slug)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = BlogPostSerializer(blog_post)
		return Response(serializer.data)
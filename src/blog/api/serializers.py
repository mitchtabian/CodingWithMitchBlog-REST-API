from rest_framework import serializers

from blog.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image',]








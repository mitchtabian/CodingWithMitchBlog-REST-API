from django.shortcuts import render
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from urllib.request import urlopen
from django.http import HttpResponse

from blog.views import get_blog_queryset
from blog.models import BlogPost

BLOG_POSTS_PER_PAGE = 10

def home_screen_view(request):
	
	context = {}

	query = ""
	query = request.GET.get('q', '')
	context['query'] = str(query)
	print("home_screen_view: " + str(query))

	blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)
	
	# Pagination
	page = request.GET.get('page', 1)
	blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)

	try:
		blog_posts = blog_posts_paginator.page(page)
	except PageNotAnInteger:
		blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
	except EmptyPage:
		blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

	context['blog_posts'] = blog_posts

	return render(request, "personal/home.html", context)




def api_view(request):
	return render(request, 'personal/api.html', {})



def raw_blogs_json_placeholder(request):

	data = urlopen("https://cdn.open-api.xyz/open-api-static/raw_json_blogs.json")
	# print(data)
	return HttpResponse(data, content_type="application/json")



def raw_user_json_placeholder(request):

	data = urlopen("https://cdn.open-api.xyz/open-api-static/raw_json_user_data.json")
	# print(data)
	return HttpResponse(data, content_type="application/json")











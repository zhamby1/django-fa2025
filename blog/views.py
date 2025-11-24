from django.shortcuts import render
from django.utils import timezone
from .models import Post

# Create your views here.

#views always take in a request, and they almost always render and return a response
def post_list(request):
    #we can query the database for all the published posts in our Post table
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #when rendering a webpage we return a render of the request, the html page we want to load, and any data we want to pass to that webpage (usually in the form of a db query)
    return render(request, 'blog/post_list.html', { 'posts' : posts})

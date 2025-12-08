from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.

#views always take in a request, and they almost always render and return a response
def post_list(request):
    #we can query the database for all the published posts in our Post table
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    #when rendering a webpage we return a render of the request, the html page we want to load, and any data we want to pass to that webpage (usually in the form of a db query)
    return render(request, 'blog/post_list.html', { 'posts' : posts})

#see one post details
def post_detail(request, pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form':form})

@login_required 
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)

    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form':form})
    

#create our list of drafts by checking if the have a publish date or not
@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts' : posts})

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
    return redirect('post_list')
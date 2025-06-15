# blog/views.py
from django.views.generic import ListView, DetailView
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    # Only show posts that are 'PUBLISHED'
    queryset = Post.objects.filter(status='PUBLISHED')
    paginate_by = 5 # Show 5 posts per page

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    # Ensure that drafts are not publicly accessible by their URL
    queryset = Post.objects.filter(status='PUBLISHED')
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
import urllib.request, json 
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings
import time

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class CacheMixin(object): #from https://gist.github.com/cyberdelia/1231560
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)



# Create your views here.
def long_run(request):
    time.sleep(10)
    return HttpResponse("hello")

@cache_page(CACHE_TTL)
def home(request):
    
    context={
        'posts':Post.objects.all()
    }
    # results = cache.get('key')
    # if results is None:
    #     print('first refresh')
    #     cache.set('key', Post.objects.all())
    #     results = cache.get('key')
    # else:
    #     print('hit')
    # context={
    #     'posts':results
    # }
    return render(request,'blog/home.html',context)

def fill_data_once():
    # url = 'https://raw.githubusercontent.com/CoreyMSchafer/code_snippets/master/Django_Blog/snippets/posts.json'
    with urllib.request.urlopen("https://raw.githubusercontent.com/CoreyMSchafer/code_snippets/master/Django_Blog/snippets/posts.json") as url:
        data = json.loads(url.read().decode())
        for d in data:
            post=Post(title=d['title'],content=d['content'],author=User.objects.filter(id=1).first())
            post.save()

class PostListView(ListView,CacheMixin):
    cache_timeout=60
    model=Post
    template_name='blog/home.html'
    context_object_name='posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView,CacheMixin):
    cache_timeout=60
    model = Post
    template_name='blog/user_post.html'
    context_object_name='posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):

    model = Post
    template_name='blog/post_detail.html'
    
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request,'blog/about.html',{'title':'About Context'})


from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
import urllib.request, json 
from django.core.cache import cache
filled=0

# Create your views here.
def home(request):
    
    # context={
    #     'posts':Post.objects.all()
    # }
    results = cache.get('key')
    if results is None:
        print('first refresh')
        cache.set('key', Post.objects.all())
        results = cache.get('key')
    else:
        print('hit')
    context={
        'posts':results
    }
    return render(request,'blog/home.html',context)

def home2(request):
    #Cached alternative, reduces 
    results = cache.get('key')
    if results is None:
        print('first refresh')
        cache.set('key', Post.objects.all().select_related())
        results = cache.get('key')
    else:
        print('hit')
    context={
        'posts':results
    }
    return render(request,'blog/home2.html',context)

def fill_data_once():
    # url = 'https://raw.githubusercontent.com/CoreyMSchafer/code_snippets/master/Django_Blog/snippets/posts.json'
    with urllib.request.urlopen("https://raw.githubusercontent.com/CoreyMSchafer/code_snippets/master/Django_Blog/snippets/posts.json") as url:
        data = json.loads(url.read().decode())
        for d in data:
            post=Post(title=d['title'],content=d['content'],author=User.objects.filter(id=1).first())
            post.save()
# fill_data_once()
class PostListView(ListView):
    results = cache.get('key')
    if results is None:
        print('first refresh')
        cache.set('key', Post.objects.all().select_related())
        results = cache.get('key')
    # results = Post.objects.all()
    queryset = results
    template_name='blog/home.html'
    context_object_name='posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name='blog/user_post.html'
    context_object_name='posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):

    # model = Post   #uncomment for normal op
    results = cache.get('key')
    if results is None:
        print('first refresh')
        cache.set('key', Post.objects.all().select_related())
        results = cache.get('key')
    # results = Post.objects.all()
    queryset = results
    template_name='blog/post_detail2.html'
    
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


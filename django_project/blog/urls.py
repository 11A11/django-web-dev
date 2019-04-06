from django.urls import path
from . import views
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView
from .views import home
urlpatterns = [
    # path('',PostListView.as_view(),name='blog-home'),
    path('',home,name='blog-home'), # this gives best performance. displays all posts at once. Performed amazing in loadtest
    path('user/<str:username>/',UserPostListView.as_view(),name='user-post'),
    path('about/',views.about,name='blog-about'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    
]

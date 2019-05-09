from django.conf.urls import url

from . import views


urlpatterns = [
    url('list', views.UsersListView.as_view(), name='users_list'),
    url('generate/', views.GenerateRandomUserView.as_view(), name='generate'),
]

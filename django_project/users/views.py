from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib .auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import redirect

from .forms import GenerateRandomUserForm
from .tasks import create_random_user_accounts
from .models import RandUser

class UsersListView(ListView):
    template_name = 'users/users_list.html'
    model = RandUser
    queryset = RandUser.objects.all()

class GenerateRandomUserView(FormView):
    template_name = 'users/generate_random_users.html'
    form_class = GenerateRandomUserForm
    queryset = User.objects.using('customers').all()

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('users_list')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form= ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form= ProfileUpdateForm(instance=request.user.profile)
    context={'u_form':u_form,'p_form':p_form}
    return render(request,'users/profile.html',context)
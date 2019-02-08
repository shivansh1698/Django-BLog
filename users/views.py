from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post


def register(request):
	if request.method=='POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			messages.success(request,"Account created for {}! You can now login ".format(username))
			return redirect('login')

	else:
		form = UserRegisterForm()
	return render(request,'users/register.html',{'form':form})



@login_required
def profile(request):

	if request.method=='POST':
		u_form=UserUpdateForm(request.POST, instance = request.user)
		p_form=ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
		messages.success(request,"Profile Updated Successfully")
		return redirect('profile')


	else:
		u_form=UserUpdateForm(instance = request.user)
		p_form=ProfileUpdateForm(instance = request.user.profile)

	context={
		'u_form':u_form,
		'p_form':p_form
	}

	return render(request,'users/profile.html',context)


class UserPostList(LoginRequiredMixin, ListView):
	model = Post
	template_name='users/posts.html'
	context_object_name = 'posts'
	ordering = ['-Date_posted']
	paginate_by = 5
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from itertools import chain
from operator import attrgetter
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Post, Profile
from .forms import PostForm, UserUpdateForm, ProfileUpdateForm, ProfilePicUpdateForm





class HomeView(ListView):
	model = Post
	template_name = 'home-page.html'
	ordering = ['-created_date']



class CreatePostView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = 'post_form.html'
	fields = ['title', 'content', 'image']

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.profile = self.request.user.profile
		return super().form_valid(form)



class UpdatePostView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Post
	template_name = 'post_form.html'
	fields = ['title', 'content', 'image']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class DeletePostView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Post
	template_name = 'delete_post.html'
	success_url = '/'


	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



class FullArticleView(LoginRequiredMixin, DetailView):
	model = Post
	template_name = 'post-page.html'



def profile_view(request):
	profile = Profile.objects.get(user=request.user)
	user = User.objects.get(username=request.user)

	context = {
		'profile' : profile,
		'user' : user
	}

	return render(request, 'profile.html', context)


def profile_update(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, "Your Profile has been successfully updated.")
			return redirect('blog:profile_view')
		messages.success(request, "Please enter valid Data.")
		return redirect('blog:profile_update')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form' : u_form,
		'p_form' : p_form
	}

	return render(request, 'profile_update.html', context)


def profile_pic_update(request):
	if request.method == 'POST':
		prof_pic_form = ProfilePicUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		profile_pic = Profile.objects.get(user=request.user)

		if prof_pic_form.is_valid():
			prof_pic_form.save()
			messages.success(request, "Your Profile Picture has been updated successfully.")
			return redirect('blog:profile_view')

	else:
		prof_pic_form = ProfilePicUpdateForm(instance=request.user.profile)
		profile_pic = Profile.objects.get(user=request.user)

		context = {
			'prof_pic_form' : prof_pic_form,
			'profile_pic' : profile_pic
		}

		return render(request, 'profile_picture_update.html', context)


from django import forms
from .models import Post, Profile
from allauth.account.forms import SignupForm	
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = Post
		fields = ['title', 'content', 'image']



class CustomSignupForm(SignupForm):
	

	def signup(self, request, user, *args, **kwargs):
		super().save()
		user_profile = user.profile
		user_profile.save()
		return user



class UserUpdateForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username', 'email']



class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['about_you', 'profession', 'mobile_number']



class ProfilePicUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['user_image']
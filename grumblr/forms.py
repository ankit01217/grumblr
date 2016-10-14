
from django import forms
from grumblr.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class PostForm(forms.ModelForm):
	desc = forms.CharField(max_length=42, label = "Desc", widget=forms.Textarea(attrs={'class': 'form-control post-input', 'placeholder': 'Insert text here...', 'rows':'5'}))
	attachment = forms.ImageField(label = "Attachment", required=False, widget=forms.FileInput())
	class Meta:
		model = Post
		fields = ['desc', 'attachment']

class AvatarForm(forms.ModelForm):
	avatar = forms.ImageField(label = "Avatar", required=False, widget=forms.FileInput(attrs={'id':'file-input','onchange':"javascript:document.getElementById('avatar-form').submit();"}))
	class Meta:
		model = UserProfile
		fields = ['avatar']

class LoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
  		super(LoginForm, self).__init__(*args, **kwargs)

  		self.base_fields['username'].widget.attrs['class'] = 'form-control login-input lower-text'
  		self.base_fields['password'].widget.attrs['class'] = 'form-control login-input'
  		self.base_fields['username'].widget.attrs['placeholder'] = 'Username'
		self.base_fields['password'].widget.attrs['placeholder'] = 'Password'
	
	class Meta:
		model = User
		fields = ['username','password']

	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		username = self.cleaned_data.get('username')
		user = User.objects.get(username__exact = username)
		if user:
			if not user.userprofile.confirmed:
				raise forms.ValidationError("Verify email to login")
				print("confirmed",user_filter[0].userprofile.confirmed)
		return cleaned_data		


class RegistrationForm(forms.ModelForm):
	firstname = forms.CharField(max_length= 20, label = "First Name", widget=forms.TextInput(attrs={'class': 'form-control login-input capitalize-text', 'placeholder': 'First Name'}))
	lastname = forms.CharField(max_length= 20, label = "Last Name", widget=forms.TextInput(attrs={'class': 'form-control login-input reg-name-item capitalize-text', 'placeholder': 'Last Name'}))
	username = forms.CharField(max_length= 20, label = "Username", widget=forms.TextInput(attrs={'class': 'form-control login-input username lower-text', 'placeholder': 'Username'}))
	email = forms.EmailField(max_length= 200, label = "Email", widget=forms.EmailInput(attrs={'class': 'form-control login-input lower-text', 'placeholder': 'Email'}))
	password = forms.CharField(max_length=200, label = "Password", widget=forms.PasswordInput(attrs={'class': 'form-control login-input', 'placeholder': 'Password'}))
	cpassword = forms.CharField(max_length=200, label = "Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control login-input', 'placeholder': 'Confrim Password'}))
	
	class Meta:
	    model = User
	    fields = ['firstname', 'lastname', 'username', 'email', 'password', 'cpassword']

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		password = cleaned_data.get('password')
		cpassword = cleaned_data.get('cpassword')
		
		if password and cpassword and password != cpassword:
			raise forms.ValidationError("Passwords did not match")
		
		return cleaned_data

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact = username):
		 	raise forms.ValidationError("Username is already taken")
		return username
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from grumblr.models import UserProfile, Post
from django.http import HttpResponse, HttpResponseRedirect,Http404
from helper import Helper
from datetime import datetime
from django.urls import reverse
from grumblr.forms import *
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction 
from webapps import settings
from django.core.mail import send_mail
from rest_framework import serializers
from grumblr.serializers import *
from rest_framework.renderers import JSONRenderer

# home page action for landing page
def home(request):
	if request.user.is_authenticated:
		return redirect('grumblr:globalstream')
	else:
		return render(request, "landing.html",{})

#register action
def register(request):
	errors = []
	context = {}
	context["errors"] = errors
	
	#GET request for register
	if request.method == 'GET':
		context["form"] = RegistrationForm()
		return render(request, "register.html", context)
	
	form = RegistrationForm(request.POST)
	context["form"] = form
	if not form.is_valid():
		return render(request, "register.html", context)

	#creates new user if no erros
	newuser = User.objects.create_user(username = form.cleaned_data['username'], password = form.cleaned_data['password'], first_name = form.cleaned_data['firstname'], last_name = form.cleaned_data['lastname'], email = form.cleaned_data['email'])
	newuser.save()

	#create random token
	token = default_token_generator.make_token(newuser)
	#create user profile object and link with newuser 
	userprofile = UserProfile(user = newuser)
	userprofile.token = token
	userprofile.save()

	#Send Confirmation Email 
	message = """Welcome to Grumblr. Please click the link below to verify the email address and complete the registraion of your account:

	http://{}{}""".format(request.get_host(), reverse("grumblr:confirm", kwargs={'username':newuser.username,'token':token}))
	subject = "Verify your email address"
	from_email = settings.EMAIL_HOST_USER
	tolist = [newuser.email]
	send_mail(subject, message, from_email, tolist, fail_silently= True)

	return render(request, "register_confirm.html", context)

		
#confirm user registration 
def confirm_registration(request, username, token):
	refuser = get_object_or_404(User, username=username)
	if not refuser.userprofile.token == token:
		raise Http404
	refuser.userprofile.confirmed = True
	refuser.userprofile.save()
	refuser.save()

	#login user automatically after registration
	login(request, refuser)
	return redirect('grumblr:globalstream')


#globalstream action
@login_required
def global_stream(request):
	#get all posts
	context = {}
	posts = Post.objects.all().order_by('-timestamp')
	context["posts"] = posts
	return render(request, "global_stream.html",context)

def global_stream_json(request):
	posts = Post.objects.all().order_by('-timestamp')
	serializer = PostSerializer(posts, many=True)
	content = JSONRenderer().render(serializer.data)
	return HttpResponse(content, content_type = 'application/json')

#friends stream action
@login_required
def friend_stream(request):
	#get all friends posts
	context = {}
	posts = Post.objects.filter(userprofile__in = request.user.userprofile.friends.all()).order_by('-timestamp')
	context["posts"] = posts
	return render(request, "friend_stream.html",context)

def friend_stream_json(request):
	posts = Post.objects.filter(userprofile__in = request.user.userprofile.friends.all()).order_by('-timestamp')
	serializer = PostSerializer(posts, many=True)
	content = JSONRenderer().render(serializer.data)
	return HttpResponse(content, content_type = 'application/json')


#profile action
@login_required
def profile(request, id):

	if request.method == "GET":
		refuser = get_object_or_404(User, id=id)
		user_posts = Post.objects.filter(userprofile=refuser.userprofile).order_by('-timestamp')
		context = {}
		context["refuser"] = refuser
		context["posts"] = user_posts
		context["follow"] = "Unfollow" if request.user.userprofile.friends.filter(user = refuser).exists() else "Follow"
		context["form"] = AvatarForm(instance=refuser.userprofile)
		return render(request, "profile.html",context)
	
	if request.method == "POST":
		if 'save' in request.POST:
			if 'firstname' in request.POST and request.POST['firstname']:
				request.user.first_name = request.POST['firstname']
			if 'lastname' in request.POST and request.POST['lastname']:
				request.user.last_name = request.POST['lastname']
			if 'age' in request.POST and request.POST['age']:
				request.user.userprofile.age = request.POST['age']
			if 'bio' in request.POST and request.POST['bio']:
				request.user.userprofile.bio = request.POST['bio']
			
			request.user.userprofile.save()
			request.user.save()
		return redirect("grumblr:profile", str(request.user.id))

def profile_posts_json(request, id):
	refuser = get_object_or_404(User, id=id)
	user_posts = Post.objects.filter(userprofile=refuser.userprofile).order_by('-timestamp')
	serializer = PostSerializer(user_posts, many=True)
	content = JSONRenderer().render(serializer.data)
	return HttpResponse(content, content_type = 'application/json')


@login_required
def follow_profile(request, id):

	if request.method == "GET":
		raise Http404 
	if request.method == "POST":
		newfriend = get_object_or_404(User, id=id)
		if not request.user.userprofile.friends.filter(user = newfriend).exists():
			#follow user
			request.user.userprofile.friends.add(newfriend.userprofile)
		else:
			#unfollw user
			request.user.userprofile.friends.remove(newfriend.userprofile)
		request.user.userprofile.save()
		request.user.save()
		return redirect("grumblr:profile", str(id))

@login_required
def add_comment(request):

	if request.method == "GET":
		raise Http404 
	if request.method == "POST":
		if not 'post_id' in request.POST or not request.POST['post_id']:
			raise ValueError('post_id required')

		post = get_object_or_404(Post, id=request.POST['post_id'])
		if 'comment' in request.POST and request.POST['comment']:
			comment = Comment(desc = request.POST['comment'], userprofile = request.user.userprofile)
			comment.save()
			post.comments.add(comment)
			post.save()
			serializer = CommentSerializer(comment)
			content = JSONRenderer().render(serializer.data)
			return HttpResponse(content, content_type = 'application/json')
		else:
			raise ValueError('comment required')	

#change avatar action
@login_required
def change_avatar(request):
	if request.method == "GET":
		raise Http404 

	if request.method == "POST":

		form  = AvatarForm(request.POST, request.FILES)
		context = {}
		context["form"] = form
		context["refuser"] = request.user
		if not form.is_valid():
			return render(request, "profile.html", context)

		request.user.userprofile.avatar = request.FILES['avatar']
		request.user.userprofile.save()
		request.user.save()
		return redirect("grumblr:profile", str(request.user.id))
	

#compose action
@login_required
def compose(request):

	errors = []
	context = {}
	context["errors"] = errors

	#GET request for register
	if request.method == 'GET':
		context["form"] = PostForm()
		return render(request, "compose.html",context)

	
	#POST request to create new user
	if 'post' in request.POST:

		form = PostForm(request.POST, request.FILES)
		context["form"] = form
		if not form.is_valid():
			return render(request, "compose.html", context)
     	
	 	#creates new post with current user
		newpost = Post(desc = form.cleaned_data['desc'], attachment = form.cleaned_data['attachment'], userprofile = request.user.userprofile, timestamp=datetime.now())
		newpost.save()

	return redirect('grumblr:globalstream')
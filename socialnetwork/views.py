from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from socialnetwork.forms import LoginForm, RegistrationForm, ProfileForm, PostForm
from socialnetwork.models import Profile, Post, Comment
from django.shortcuts import get_object_or_404
from django.core import serializers
import json
import dateutil.parser

@login_required
def global_stream(request):
    context = dict()
    context['page_name'] = "Global Stream"
    p = get_object_or_404(Profile, profile_user = request.user)

    if request.method == "POST":
        # create post
        new_post = Post()
        new_post_form = PostForm(request.POST, instance=new_post)
        new_post.post_date_time = timezone.now()
        new_post.post_profile = p

        if not new_post_form.is_valid():
            context['post_form'] = new_post_form
            return render(request, 'socialnetwork/global_stream.html', context)

        new_post_form.save()
        context['message'] = "Post created"
    

    # display all posts
    context['post_form'] = PostForm()
    # context['all_posts'] = Post.objects.order_by('post_date_time').reverse()
    return render(request, 'socialnetwork/global_stream.html', context)

def refresh_global(request):
    if 'last_refresh' not in request.GET: 
        return HttpResponseNotFound('<h1>Missing parameters</h1>')
    
    last_refresh = dateutil.parser.parse(request.GET['last_refresh'])

    
    posts = list()
    all_posts_q = Post.objects.filter(post_date_time__gte=last_refresh)
    all_posts_q = all_posts_q.order_by('post_date_time') #.reverse()
    for post in all_posts_q:
        posts.append({
            'id': post.id,
            'text': post.post_input_text,
            'user_name': post.post_profile.profile_user.username,
            'full_name': post.post_profile.profile_user.get_full_name(),
            'post_time': str(post.post_date_time.strftime("%m/%d/%Y %H:%M"))
        })


    comments = list()
    all_comments_q = Comment.objects.filter(comment_date_time__gte=last_refresh)
    all_comments_q = all_comments_q.order_by('comment_date_time') #.reverse()
    for comment in all_comments_q:
        comments.append({
            'id': comment.id,
            'post_id': comment.comment_post.id,
            'text': comment.comment_input_text,
            'user_name': comment.comment_profile.profile_user.username,
            'full_name': comment.comment_profile.profile_user.get_full_name(),
            'comment_time': str(comment.comment_date_time.strftime("%m/%d/%Y %H:%M"))
        })

    response_text = json.dumps({ 'posts': posts, 'comments': comments, 
                               'last_refresh': str(timezone.now())})

    return HttpResponse(response_text, content_type='application/json')

@login_required
def follower_stream(request):
    context = dict()
    context['page_name'] = "Follower Stream"
    p = get_object_or_404(Profile, profile_user = request.user)

    if request.method == "POST":
        # create post
        new_post = Post()
        new_post_form = PostForm(request.POST, instance=new_post)
        new_post.post_date_time = timezone.now()
        new_post.post_profile = p

        if not new_post_form.is_valid():
            context['post_form'] = new_post_form
            return render(request, 'socialnetwork/follower_stream.html', context)

        new_post_form.save()
        context['message'] = "Post created"
    

    # display all posts
    context['post_form'] = PostForm()
    all_posts = Post.objects.order_by('post_date_time').reverse()
    # context['all_posts'] = all_posts.filter(post_profile__in = p.following.all())
    return render(request, 'socialnetwork/global_stream.html', context)

def refresh_follower(request):
    p = get_object_or_404(Profile, profile_user = request.user)
    
    if 'last_refresh' not in request.GET: 
        return HttpResponseNotFound('<h1>Missing parameters</h1>')
    
    last_refresh = dateutil.parser.parse(request.GET['last_refresh'])

    
    posts = list()
    all_posts_q = Post.objects.filter(post_date_time__gte=last_refresh)
    all_posts_q = all_posts_q.order_by('post_date_time') #.reverse()
    all_posts_q = all_posts_q.filter(post_profile__in = p.following.all())
    for post in all_posts_q:
        posts.append({
            'id': post.id,
            'text': post.post_input_text,
            'user_name': post.post_profile.profile_user.username,
            'full_name': post.post_profile.profile_user.get_full_name(),
            'post_time': str(post.post_date_time.strftime("%m/%d/%Y %H:%M"))
        })


    comments = list()
    all_comments_q = Comment.objects.filter(comment_date_time__gte=last_refresh)
    all_comments_q = all_comments_q.order_by('comment_date_time') #.reverse()
    all_comments_q = all_comments_q.filter(comment_post__in = all_posts_q)
    for comment in all_comments_q:
        comments.append({
            'id': comment.id,
            'post_id': comment.comment_post.id,
            'text': comment.comment_input_text,
            'user_name': comment.comment_profile.profile_user.username,
            'full_name': comment.comment_profile.profile_user.get_full_name(),
            'comment_time': str(comment.comment_date_time.strftime("%m/%d/%Y %H:%M"))
        })

    response_text = json.dumps({ 'posts': posts, 'comments': comments, 
                               'last_refresh': str(timezone.now())})

    return HttpResponse(response_text, content_type='application/json')

@login_required
def add_comment(request):
    if ((request.method != "POST") or 
        ('comment_text' not in request.POST) or
        ('post_id' not in request.POST)):
        return HttpResponseNotFound('<h1>Missing parameters</h1>')

    p = get_object_or_404(Profile, profile_user = request.user)
    post = get_object_or_404(Post, id = request.POST['post_id'])

    # create comment
    new_comment = Comment()
    new_comment.comment_date_time = timezone.now()
    new_comment.comment_profile = p
    new_comment.comment_input_text = request.POST['comment_text']
    new_comment.comment_post = post

    new_comment.save()

    return HttpResponse("", content_type='application/json')

@login_required
def profile(request):
    return profile_id(request, request.user.get_username())

@login_required
def profile_pk(request, profile_pk = 0):
    p = get_object_or_404(Profile, id = pk)
    return profile_id(request, p.profile_user.username)


@login_required
def profile_id(request, username = ""):
    context = dict()

    # attempt to get user object and profile for that username
    u = get_object_or_404(User, username=username)
    p = get_object_or_404(Profile, profile_user = u)
    curr_u_profile = get_object_or_404(Profile, profile_user = request.user)

    # format the page title
    context['page_name'] = "Profile Page for {}".format(u.get_full_name())
    context['other_user'] = p
    context['all_following'] = curr_u_profile.following.all()
    context['has_picture'] = p.profile_picture

    # GET request
    if (request.method == 'GET'):
        if request.user.get_username() == username:
            # profile page is for logged in user
            context['profile_form'] = ProfileForm(instance=p)
        else:
            # profile page is for some other user
            context['other_user'] = p
            if p in curr_u_profile.following.all(): 
                context['follow_label'] = "unfollow"
            else:
                context['follow_label'] = "follow"

        # return redirect(reverse('profile', args=(,)))
        return render(request, 'socialnetwork/profile.html', context)

    # POST method
    if request.user.get_username() == username:
        # user has changed own profile
        profile_form = ProfileForm(request.POST, request.FILES, instance=p)
        context['profile_form'] = profile_form
        if not profile_form.is_valid(): 
            return render(request, 'socialnetwork/profile.html', context)

        picture = profile_form.cleaned_data['profile_picture']
        if picture: p.image_type = picture.content_type
        profile_form.save()
        return render(request, 'socialnetwork/profile.html', context)

    else:
        # user has (un)followed other user
        if p in curr_u_profile.following.all(): 
            curr_u_profile.following.remove(p)
            context['follow_label'] = "follow"
        else:
            curr_u_profile.following.add(p)
            context['follow_label'] = "unfollow"


    return render(request, 'socialnetwork/profile.html', context)


@login_required
def profile_picture(request, username = ""):
    # find user
    try:
        u = get_object_or_404(User, username=username)
        p = get_object_or_404(Profile, profile_user = u)
        return HttpResponse(p.profile_picture, content_type=p.image_type)
    # username does not exist or does not have picture: default img
    except:
        context = dict()
        context['message'] = "No such image or user"
        # sending response 
        return render(request, 'socialnetwork/base.html', context)
        # username 
        # return HttpResponse(item.picture, content_type=item.content_type)


def login_user(request):
    context = dict()
    context['page_name'] = "Login"
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('home'))

def register_user(request):
    context = dict()
    context['page_name'] = "Register"
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)

    # create profile
    new_profile = Profile()
    new_profile.profile_user = new_user
    new_profile.save()

    return redirect(reverse('home'))
    # return global_stream(request)

def logout_user(request):
    logout(request)
    return login_user(request)



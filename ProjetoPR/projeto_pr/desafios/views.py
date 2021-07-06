from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, get_object_or_404
from django.contrib.auth.forms import User
from django.contrib import messages
from .models import Challenge, Comment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def index(request):
    return render(request, 'desafios/index.html')


@login_required(login_url="/accounts/login/")
def user_homepage(request):
    return render(request, 'desafios/user_homepage.html')


def sign_up(request):
    if request.method == 'POST':
        if request.POST['username']:
            username = request.POST['username']
        else:
            messages.info(request, 'Username field empty!')
            return redirect('desafios:sign_up')
        if request.POST['first_name']:
            first_name = request.POST['first_name']
        else:
            messages.info(request, 'First name field empty!')
            return redirect('desafios:sign_up')
        if request.POST['last_name']:
            last_name = request.POST['last_name']
        else:
            messages.info(request, 'Last name field empty!')
            return redirect('desafios:sign_up')
        if request.POST['email']:
            email = request.POST['email']
        else:
            messages.info(request, 'Email field empty!')
            return redirect('desafios:sign_up')
        if request.POST['password1']:
            password1 = request.POST['password1']
        else:
            messages.info(request, 'Password field empty!')
            return redirect('desafios:sign_up')
        if request.POST['password2']:
            password2 = request.POST['password2']
        else:
            messages.info(request, 'Password confirmation field empty!')
            return redirect('desafios:sign_up')
        if password1 == password2:
            if len(password1) < 5:
                messages.info(request, 'Password to small, must have 5 characters')
                return redirect('desafios:sign_up')
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('desafios:sign_up')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('desafios:sign_up')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password1)
                user.save()
                new_user = authenticate(username=username, password=password1)
                login(request, new_user)
                return render(request, 'desafios/user_homepage.html')
        else:
            messages.info(request, 'Password is not matching')
            return redirect('desafios:sign_up')
    return render(request, 'desafios/signuppage.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('desafios:user_homepage')
        else:
            messages.info(request, 'Username or Password incorrect')
    return render(request, 'desafios/loginpage.html')


@login_required(login_url="/accounts/login/")
def log_out(request):
    logout(request)
    return redirect('desafios:index')


@login_required(login_url="/accounts/login/")
def create_challenge(request, challenge_type):
    section = 0
    tag_text = 'challenge-{}'
    tag_text = tag_text.format(Challenge.objects.count())
    if request.GET['createbutton'] == 'image':
        section = 1
    elif request.GET['createbutton'] == 'link':
        section = 2
    if request.method == 'POST':
        title = request.POST['title1']
        content = request.POST['content']
        image = request.POST['image']
        if request.POST['video']:
            embed = request.POST['video']
            embed = embed.split("embed/")
            embed = embed[1].split(" frameborder")
            video = embed[0]
            video = video[:-1]
        else:
            video = None
        new_challenge = Challenge(title=title, content=content, challenge_type=challenge_type, tag=tag_text,
                                  image=image, video=video, challenge_user=request.user)
        new_challenge.save()
        return HttpResponseRedirect(reverse('desafios:challenges', args=(challenge_type,)))
    return render(request, 'desafios/create_challenge.html', {'section': section, 'challenge_type': challenge_type})


@login_required(login_url="/accounts/login/")
def challenges_views(request, challenge_type):
    challenge_type1 = str(challenge_type)
    challenge_list = Challenge.objects.filter(challenge_type__exact=challenge_type).order_by('date').reverse()
    x = 1
    if request.method == 'POST':
        if request.POST['order'] == 'top':
            x = 2
            challenge_list = Challenge.objects.filter(challenge_type__exact=challenge_type).annotate(likes_count=Count('challenge_likes')).order_by('-likes_count')
    return render(request, 'desafios/challenges.html',
                  {'challenge_type': challenge_type1, 'challenge_list': challenge_list, 'x': x})


@login_required(login_url="/accounts/login/")
def challenge_like_upvote(request, challenge_type):
    challenge = get_object_or_404(Challenge, id=request.POST.get('id'))
    if challenge.challenge_likes.filter(id=request.user.id).exists():
        pass
    else:
        challenge.challenge_likes.add(request.user)
    if request.is_ajax():
        y = 1
        challenge_likes = challenge.get_challenge_likes()
        return JsonResponse({'challenge_likes': challenge_likes, 'y': y})


@login_required(login_url="/accounts/login/")
def challenge_like_downvote(request, challenge_type):
    challenge = get_object_or_404(Challenge, id=request.POST.get('id'))
    challenge.challenge_likes.remove(request.user)
    if request.is_ajax():
        y = 2
        challenge_likes = challenge.get_challenge_likes()
        return JsonResponse({'challenge_likes': challenge_likes, 'y': y})


def comments(request, challenge_tag):
    challenge = Challenge.objects.filter(tag__exact=challenge_tag).get()
    challenge_comments = Comment.objects.filter(comment_challenge__exact=challenge.id).order_by('comment_date').reverse()
    return render(request, 'desafios/comments.html', {'challenge': challenge, 'comments': challenge_comments})


def post_comment(request, challenge_tag):
    if request.method == 'POST':
        challenge = Challenge.objects.filter(tag__exact=challenge_tag).get()
        new_comment = Comment(comment_user=request.user, comment_challenge=challenge, text=request.POST['content'])
        new_comment.save()
        return HttpResponseRedirect(reverse('desafios:comments', args=(challenge_tag,)))
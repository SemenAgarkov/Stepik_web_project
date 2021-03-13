from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user

from qa.models import Question, Answer, Session, do_login
from qa.forms import AnswerForm, AskForm, SignupForm, LoginForm

from datetime import datetime, timedelta

def test(request, *args, **kwargs):
    return HttpResponse('OK')

def index(request):
    try:
        page = int(request.GET.get("page"))
    except ValueError:
        page = 1
    except TypeError:
        page = 1
    questions = Question.objects.all().order_by('-id')
    paginator = Paginator(questions, 10)
    page = paginator.page(page)

    return render(request, 'list.html',
            {'title': 'Latest',
            'paginator': paginator,
             'questions': page.object_list,
             'page': page,})

def question(request, num,):
    try:
        q = Question.objects.get(id=num)
    except Question.DoesNotExist:
        raise Http404
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            _ = form.save()
            url = q.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': q.id})

    return render(request, 'question.html', {'question': q,
                                             'form': form,
                                             'user': request.user,
                                             'session': request.session,
                                             })

def popular(request):
    try:
        page = int(request.GET.get("page"))
    except ValueError:
        page = 1
    except TypeError:
        page = 1
    questions = Question.objects.all().order_by('-rating')
    paginator = Paginator(questions, 10)
    page = paginator.page(page)

    return render(request, 'list.html',
                  {'title': 'Popular',
                   'paginator': paginator,
                   'questions': page.object_list,
                   'page': page, })

def ask(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            form._user = request.user
            post = form.save()
            url = post.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'ask.html', {'form': form,
                                        'user': request.user,
                                        'session': request.session,})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.clean()
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def check_login(login, password):
    try:
        user = User.objects.get(username=login)
    except Exception:
        return None
    if user.password != password:
        return None
    return user

def user_login(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = check_login(username, password)
        url = request.POST.get('continue', '/')
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(url)
        else:
            error = u'Wrong login / password'

    return render(request, 'login.html', {'form': LoginForm(), 'error': error})


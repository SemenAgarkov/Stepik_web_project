from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login

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
            question = form.save()
            url = '/'
            return HttpResponseRedirect(url)
    else:
        form = SignupForm()
    return render(request, 'signup.html', {
        'form': form,
    })

def login(request):
    error = ''
    if request.method == 'POST':
        login = request.POST.get('username')
        password = request.POST.get('password')
        url = '/'
        sessid = do_login(login, password)
        if sessid:
            response = HttpResponseRedirect(url)
            response.set_cookie('sessid', sessid,
                httponly=True,
                expires = datetime.now()+timedelta(days=5)
                )
            return response
        else:
            error = u'Wrong login / password'
    form = LoginForm()
    return render(request, 'login.html', {'error': error, 'form': form })

'''
def do_login(username, password):
    try:
        user = User.objects.get(login=username)
    except User.DoesNotExist:
        return None
    hashed_pass = salt_and_hash(password)
    if user.password != hashed_pass
        return None
    session = Session()
    session.key = generate_long_random_key()
    session.user = user
    session.expires = datetime.now() + timedelta(days=5)
    session.save()
    return session.key
'''

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.db.models import Count
from django.contrib import messages
from .models import Question, Answer, Like

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Login failed. Please check your username and password.')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    questions = Question.objects.all().exclude(user=request.user)
    return render(request, 'home.html', {'questions': questions})


@login_required(login_url='login')
def create_question(request):
    if request.method == 'POST':
        text = request.POST['text']
        Question.objects.create(user=request.user, text=text)
        return redirect('home')
    return render(request, 'create_question.html')


def my_question(request):
    questions = Question.objects.filter(user=request.user)
    return render(request, "my_question.html",{"questions":questions})


@login_required(login_url='login')
def answer_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        text = request.POST['text']
        Answer.objects.create(user=request.user, question=question, text=text)
        return redirect('home')
    return render(request, 'answer_question.html', {'question': question})

@login_required(login_url='login')
def view_all_answer(request, question_id):
    answers = Answer.objects.filter(question=question_id).select_related('user').annotate(like_count=Count('like'))
    return render(request, 'answers.html',{'answer': answers})


@login_required(login_url='login')
def like_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    Like.objects.create(user=request.user, answer=answer)

    return redirect('home')
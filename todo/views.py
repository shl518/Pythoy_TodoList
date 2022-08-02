from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import datetime

month_dic = months = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}


# Create your views here.
def home(request):
    today = datetime.date.today()
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    if str(request.user) == 'AnonymousUser':
        unstart = current = completed = expired = 0
    else:
        Todo.objects.filter(user=request.user, isDaily=True, datecompleted__lt=today).update(datecompleted=None,
                                                                                             overdue=False)
        unstart = Todo.objects.filter(user=request.user, overdue=False, status=0, expiration_date__lt=tomorrow).count()
        current = Todo.objects.filter(user=request.user, overdue=False, status=1, expiration_date__lt=tomorrow).count()
        completed = Todo.objects.filter(user=request.user, datecompleted__isnull=False, expiration_date__gte=today,
                                        expiration_date__lt=tomorrow).count()
        expired = Todo.objects.filter(user=request.user, overdue=True, expiration_date__lt=tomorrow,
                                      datecompleted__isnull=True, expiration_date__gte=today).count()
    return render(request, 'todo/home.html', {
        'user_name': str(request.user),
        'unstart': unstart,
        'current': current,
        'completed': completed,
        'expired': expired,
        'all': unstart + completed + current + expired,
    })


# User Sign up
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        try:
            if (request.POST['password1'] == request.POST['password2']):
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')

        except IntegrityError:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),
                                                            'error': 'That username is already been taken. Please choose a new username.'})
        else:
            return render(request, 'todo/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Passwords did not match.'})


# User Login
def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        # here we allowed only POST request, so user can logged in via POST request only
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match.'})
        else:
            login(request, user)
            return redirect('home')


# calendar
def tocalendar(request):
    return render(request, 'todo/calendar.html')


def whichdate(request):
    global month_dic
    date_list = list(request.GET.values())
    date = str(date_list[1] + "-%02d-%02d" % (month_dic[date_list[0]], int(date_list[2])))
    all_day = Todo.objects.filter(user=request.user)
    matters = []
    for item in all_day:
        if str(item.expiration_date).split()[0] == date:
            matters.append(item)
    print(matters)
    return render(request, 'todo/calendar.html')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',
                          {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})


@login_required
def currenttodos(request):
    data_dict = {}
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    start = request.GET.get('start')
    end = request.GET.get('end')
    data_dict['expiration_date__lt'] = tomorrow
    if start and end:
        today = str(datetime.date.today())
        start = today + ' ' + start + ':00'
        end = today + ' ' + end + ':00'
        data_dict['expiration_date__lt'] = end
        data_dict['expiration_date__gt'] = start
    data_dict['overdue'] = False
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True, status__lt=2, **data_dict)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def unstarttodos(request):
    data_dict = {}
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    start = request.GET.get('start')
    end = request.GET.get('end')
    if start and end:
        data_dict['expiration_date__lt'] = end
        data_dict['expiration_date__gt'] = start
    data_dict['status'] = 0
    data_dict['overdue'] = False
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True, expiration_date__gte=tomorrow,
                                **data_dict)
    return render(request, 'todo/unstarttodo.html', {'todos': todos})


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos})


@login_required
def expiredtodos(request):
    now = datetime.datetime.now()
    Todo.objects.filter(user=request.user, expiration_date__lt=now, overdue=False).update(overdue=True)
    todos = Todo.objects.filter(user=request.user, expiration_date__lt=now, datecompleted__isnull=True).order_by(
        '-expiration_date')
    return render(request, 'todo/expiredtido.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        pre = str(todo.expiration_date)[0:19]
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'pre': pre})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad Info.'})


@login_required
def completetodo(request):
    todo_pk = request.GET.get('nid')
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    todo.status = todo.status + 1
    if todo.status == 2:
        todo.datecompleted = timezone.now()
    todo.save()
    return redirect('currenttodos')


@login_required
def deletetodo(request):
    todo_pk = request.GET.get('nid')
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    todo.delete()
    return redirect('currenttodos')

import functools

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import response
from django.forms.models import model_to_dict
import datetime
from todo.pack import greater
from utils.algorithm import scheduling
from django.contrib import messages

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
    if str(request.user) == 'AnonymousUser':
        request.session['auto'] = False
    auto = request.session['auto']
    today = datetime.date.today()
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    if str(request.user) == 'AnonymousUser':
        unstart = current = completed = expired = 0
    else:
        ###############
        todos = Todo.objects.filter(user=request.user, isDaily=True, expiration_date__lt=today)
        for to in todos:
            end1 = str(today) + ' ' + str(to.fixedTime_end)
            if to.fixedTime_end:
                to.expiration_date = end1
                to.status = 0
                to.datecompleted = None
                to.save()
        t = Todo.objects.filter(user=request.user)
        # for i in t:
        #     i.assign_end = '00:00'
        #     i.assign_start = '00:00'
        #     i.status = 0
        #     i.datecompleted = None
        #     i.save()
        ###############
        unstart = Todo.objects.filter(user=request.user, status=0, expiration_date__lt=tomorrow).count()
        current = Todo.objects.filter(user=request.user, status=1, expiration_date__lt=tomorrow).count()
        completed = Todo.objects.filter(user=request.user, datecompleted__isnull=False, expiration_date__gte=today,
                                        expiration_date__lt=tomorrow).count()
        expired = Todo.objects.filter(user=request.user, status=3, expiration_date__lt=tomorrow,
                                      datecompleted__isnull=True, expiration_date__gte=today).count()
    return render(request, 'todo/home.html', {
        'user_name': str(request.user),
        'unstart': unstart,
        'current': current,
        'completed': completed,
        'expired': expired,
        'all': unstart + completed + current + expired,
        'auto': auto,
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
                return redirect('home')

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
        item_date = str(item.expiration_date).split()[0]
        create_date = str(item.created).split()[0]
        query_date = [int(date_list[1]), month_dic[date_list[0]], int(date_list[2])]
        if (item_date == date) or (item.isDaily and
                                   greater(list(map(int, create_date.split('-'))), query_date)):
            matters.append(item)
    arranged = arrange(matters)
    json_list = []
    for item in arranged:
        json_list.append(model_to_dict(item))
    return response.JsonResponse(json_list, safe=False)


def today(request):
    date_list = list(request.GET.values())
    date = str(date_list[1] + "-%02d-%02d" % (int(date_list[0]), int(date_list[2])))
    all_day = Todo.objects.filter(user=request.user)
    matters = []
    for item in all_day:
        item_date = str(item.expiration_date).split()[0]
        query_date = [int(date_list[1]), int(date_list[0]), int(date_list[2])]
        if (item_date == date) or (item.isDaily and
                                   greater(list(map(int, item_date.split('-'))), query_date)):
            matters.append(item)
    arranged = arrange(matters)
    json_list = []
    for item in arranged:
        json_list.append(model_to_dict(item))
    return response.JsonResponse(json_list, safe=False)


def cmp_for_todo(self, other):
    time_1 = self["expiration_date"]
    time_2 = other["expiration_date"]
    duration_1 = str("%02d" % self["predict_hour"]) + ":" + str("%02d" % self["predict_minute"])
    duration_2 = str("%02d" % other["predict_hour"]) + ":" + str("%02d" % other["predict_minute"])
    if time_1 > time_2:
        return 1
    elif time_1 < time_2:
        return -1
    else:
        if duration_1 > duration_2:
            return 1
        elif duration_1 < duration_2:
            return -1
        else:
            return 0


def arrange(all_todos):
    other_todos = []
    cur_todos = []
    for item in all_todos:
        # print(item.title + " : " + str(item.datecompleted))
        if (item.datecompleted is None) & (item.status < 2):
            cur_todos.append(item)
        else:
            other_todos.append(item)
    assign_time = scheduling(cur_todos)
    for i in range(min(len(assign_time), len(cur_todos))):
        if cur_todos[assign_time[i]['id'] - 1].assign_start == '00:00' or \
                cur_todos[assign_time[i]['id'] - 1].assign_end == '00:00':
            cur_todos[assign_time[i]['id'] - 1].assign_start = assign_time[i]['start']
            cur_todos[assign_time[i]['id'] - 1].assign_end = assign_time[i]['end']
    for item in other_todos:
        cur_todos.append(item)
    return cur_todos


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def createtodo(request):
    auto = request.session['auto']
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'auto': auto})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            if newtodo.isDaily:
                today = datetime.date.today()
                end1 = str(today) + ' ' + str(newtodo.fixedTime_end)
                newtodo.expiration_date = end1
            if len(str(newtodo.fixedTime_start).split(':')) == 3:
                h, m, s = str(newtodo.fixedTime_start).split(':')
                start = int(h) * 60 + int(m)
                h, m, s = str(newtodo.fixedTime_end).split(':')
                end = int(h) * 60 + int(m)
                if start > end:
                    messages.warning(request, "日常任务固定开始时间大于结束时间，请您重新填写！")
                    return render(request, 'todo/createtodo.html', {'auto': auto})
            print(newtodo.fixedTime_start, newtodo.fixedTime_end)

            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html',
                          {'form': TodoForm(), 'error': 'Bad data passed in. Try again.', 'auto': auto})


@login_required
def currenttodos(request):
    auto = request.session['auto']
    print(auto)
    data_dict = {}
    today = datetime.date.today()
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    start = request.GET.get('start')
    end = request.GET.get('end')
    data_dict['expiration_date__gt'] = today
    data_dict['expiration_date__lt'] = tomorrow
    if start and end:
        today = str(datetime.date.today())
        start = today + ' ' + start + ':00'
        end = today + ' ' + end + ':00'
        data_dict['expiration_date__lt'] = end
        data_dict['expiration_date__gt'] = start
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True, status__lt=2, **data_dict)
    assign_time = scheduling(list(todos))
    for i in range(min(len(assign_time), len(todos))):
        todos[assign_time[i]['id'] - 1].assign_start = assign_time[i]['start']
        todos[assign_time[i]['id'] - 1].assign_end = assign_time[i]['end']
    flag = 0
    if len(assign_time) != len(todos):
        flag = 1
    return render(request, 'todo/currenttodos.html', {'todos': todos, 'flag': flag, 'auto': auto})


@login_required
def unstarttodos(request):
    auto = request.session['auto']
    data_dict = {}
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    start = request.GET.get('start')
    end = request.GET.get('end')
    if start and end:
        data_dict['expiration_date__lt'] = end
        data_dict['expiration_date__gt'] = start
    data_dict['status'] = 0
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True, expiration_date__gte=tomorrow,
                                **data_dict)
    return render(request, 'todo/unstarttodo.html', {'todos': todos, 'auto': auto})


@login_required
def completedtodos(request):
    auto = request.session['auto']
    data_dict = {}
    today = datetime.date.today()
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    data_dict['expiration_date__gt'] = today
    data_dict['expiration_date__lt'] = tomorrow
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False, status=2, **data_dict).order_by(
        '-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos, 'auto': auto})


@login_required
def expiredtodos(request):
    auto = request.session['auto']
    todos = Todo.objects.filter(user=request.user, status=3).order_by(
        '-expiration_date')
    return render(request, 'todo/expiredtido.html', {'todos': todos, 'auto': auto})


@login_required
def viewtodo(request, todo_pk):
    auto = request.session['auto']
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        pre = str(todo.expiration_date)[0:19]
        s_time = str(todo.fixedTime_start)[0:5]
        e_time = str(todo.fixedTime_end)[0:5]
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'pre': pre,
                                                      's_time': s_time, 'e_time': e_time, 'auto': auto})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html',
                          {'todo': todo, 'form': form, 'error': 'Bad Info.', 'auto': auto})


@login_required
def completetodo(request):
    todo_pk = request.GET.get('nid')
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    todo.status = todo.status + 1
    print(timezone.now())
    if todo.status == 1:
        todo.assign_start = str(timezone.now())[11:16]
    if todo.status == 2:
        todo.datecompleted = timezone.now()
        todo.assign_end = str(timezone.now())[11:16]
    todo.save()
    return redirect('currenttodos')


@login_required
def deletetodo(request):
    todo_pk = request.GET.get('nid')
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    todo.delete()
    return redirect('currenttodos')


@login_required
def changetodo(request):
    status = request.GET.get("n")
    request.session['auto'] = status
    return response.JsonResponse(status, safe=False)

from django.contrib import admin
from django.urls import path
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    # todos
    path('', views.home, name='home'),
    path('create/', views.createtodo, name='createtodo'),
    path('current/', views.currenttodos, name='currenttodos'),
    path('completed/', views.completedtodos, name='completedtodos'),
    path('todo/<int:todo_pk>', views.viewtodo, name='viewtodo'),
    path('todo/<int:todo_pk>/complete', views.completetodo, name='completetodo'),
    path('todo/<int:todo_pk>/delete', views.deletetodo, name='deletetodo'),
    path('unstart/', views.unstarttodos, name='unstarttodos'),
    path('expired/', views.expiredtodos, name='expiredtodos'),
    path('run/', views.completetodo, name='completetodo'),
    path('remove/', views.deletetodo, name='deletetodo'),
    path('change/', views.changetodo, name='changetodo'),

    # calendar
    path('calendar/', views.tocalendar, name='tocalendar'),
    path('calendar/whichdate/', views.whichdate, name='whichdate'),
    path('calendar/today/', views.today, name='today'),
]

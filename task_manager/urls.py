from django.conf.urls import patterns, include, url
from django.contrib import admin

from TaskMan.views import TasksDetailView, register_user, user_login, user_logout, \
                          create_task, UserTasksView, DeleteTaskView, TasksEditView, TaskUpdateView, \
                          tasks_sort_view, tasks_collection, task_detail, history_view, home

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^history/$', history_view, name='history'),
    url(r'^$', home, name='home'),
    url(r'^taskman/tasks/$', TasksDetailView.as_view(), name='tasks'),
    url(r'^taskman/register/$', register_user, name='register'),
    url(r'^taskman/login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^taskman/create_tasks/$', create_task, name='create_tasks'),
    url(r'^taskman/user_tasks/$', UserTasksView.as_view(), name='user_tasks'),
    url(r'^taskman/tasks/edit/$', TasksEditView.as_view(), name='edit_tasks'),
    url(r'^taskman/tasks/update/$', TaskUpdateView.as_view(), name='update_task'),
    url(r'^taskman/tasks/sort/$', tasks_sort_view, name='sort_task'),
    url(r'^taskman/delete/(?P<pk>\d+)/$', DeleteTaskView.as_view(), name='delete_task'),
    url(r'^api/v1/tasks/$', tasks_collection, name='tasks_collection'),
    url(r'^api/v1/tasks/(?P<pk>[0-9]+)$', task_detail, name='task_detail'),
)

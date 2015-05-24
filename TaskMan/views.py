import collections
import json

from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.views.generic import View, ListView
from django.views.generic.edit import DeleteView
from django.contrib.admin.models import LogEntry

# Rest frame Work
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from TaskMan.serializers import TasksSerializer

from TaskMan.forms import UserCreationForm, TasksCreationForm
from TaskMan.models import Tasks
from TaskMan import constants

def register_user(request):
    
    context = RequestContext(request)
    already_registered = False

    if request.method == 'POST':
        user_form = UserCreationForm(data=request.POST)
        if user_form.is_valid():
	        user = user_form.save()
	        already_registered = True
        else:
            print user_form.errors
    else:
        user_form = UserCreationForm()
    return render_to_response('TaskMan/register.html',
			      {'user_form': user_form, 'registered': already_registered}, context)


def user_login(request):
    
    context = RequestContext(request)
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/taskman/user_tasks/', )
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(email, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('TaskMan/login.html', {}, context)
        
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
        
def create_task(request):
    
    context = RequestContext(request)
    if request.method == 'POST':
        tasks_form = TasksCreationForm(data=request.POST, request=request)
        user = request.user
        if tasks_form.is_valid():
            if user:
                tasks_form.save()
                return HttpResponseRedirect('/taskman/user_tasks/',)
            else:
                return HttpResponse("You are Not Authorized to Create task.")
    else:
        tasks_form = TasksCreationForm(request=request)
    return render_to_response('TaskMan/create_task.html', {'task_form': tasks_form}, context)
    
class UserTasksView(ListView):

    model = Tasks
    template_name = 'TaskMan/user_task.html'
    context_object_name = 'user_tasks'
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super(UserTasksView, self).get_context_data(**kwargs)
        return context
 
def home(request):
    context = RequestContext(request)
    return render_to_response('TaskMan/home.html', {}, context)
    
    
class TasksDetailView(ListView):
    
    model = Tasks
    template_name = 'TaskMan/tasks.html'
    context_object_name = 'all_tasks'
   
    def get_context_data(self, **kwargs):
        context = super(TasksDetailView, self).get_context_data(**kwargs)
        return context
        
class DeleteTaskView(DeleteView):

    model = Tasks
    success_url = reverse_lazy('user_tasks')
    
    
class TasksEditView(ListView):
    
    model = Tasks
    template_name = 'TaskMan/edit.html'
    context_object_name = 'available_tasks'
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(TasksEditView, self).get_context_data(**kwargs)
        return context
        

class TaskUpdateView(View):
    """ Task Update View For Specific User"""
    def post(self, request):
        all_updated_val = request.POST.getlist('getlist_val')
        request_dict = {}
        for item in all_updated_val:
            request_dict.update({int(item.split('_')[1]):item.split('_')[0]})
        all_tasks = Tasks.objects.filter(user=request.user)
        for task in all_tasks:
            if task.is_completed != request_dict.get(task.id):
                task.is_completed = request_dict.get(task.id)
                task.save()
        return HttpResponseRedirect('/taskman/user_tasks/', )  
        
        
def tasks_sort_view(request):
    """ Task Sort View For Specific User"""
    
    if request.is_ajax():
        sorted_by = constants.SEARCH_KEY.get(request.GET['sort_key'])
        if sorted_by:
            all_tasks = Tasks.objects.order_by('-'+sorted_by).filter(user=request.user)
            tasks_dict = []
            for item in all_tasks:
                tasks_dict.append({
                    'name': item.task,
                    'created_date': item.created_date.strftime('%d %B, %y'),
                    'status': item.is_completed,
                    'task_id': item.id,
                    'deat_line_date': item.dead_line_date.strftime('%d %B, %y')
                })
            return HttpResponse(json.dumps(tasks_dict), content_type='application/json')      

# DASH_BOARD
def history_view(request):
    log = LogEntry.objects.select_related().all().order_by("id")
    return render_to_response("TaskMan/history.html", {'log': log},)

# API VIEWS  
@api_view(['GET', 'POST'])
def tasks_collection(request):
    """
    Get all tasks, or add a specific task
    """
    if request.method == 'GET':
        tasks = Tasks.objects.all()
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TasksSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    """
    Get, udpate, or delete a specific task, require user, dead_line_date, task
    """
    try:
        task = Tasks.objects.get(pk=pk)
    except Tasks.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'GET':
        serializer = TasksSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TasksSerializer(task, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        message = "Deleted with task Name: %s, and task ID: %d" %(task.task, task.id) 
        response_message = {'Record': message}
        task.delete()
        return Response(response_message, status=status.HTTP_200_OK)

        

from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm , TaskForm
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import Task

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import TaskSerializer

# Create your views here.
def home(request): 
	return render(request, 'baseapp/home.html', {})

def login_user (request):
	if request.method == 'POST': #if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request,('Youre logged in'))
			return redirect('home')   
		else:
			messages.success(request,('Error logging in'))
			return redirect('login') 
	else:
		return render(request, 'baseapp/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request,('Youre now logged out'))
	return redirect('home')

def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			#group = form.cleaned_data.get('group')
			#user.groups.add(group) 
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ('Youre now registered'))
			return redirect('home')
	else: 
		form = SignUpForm() 

	context = {'form': form}
	return render(request, 'baseapp/register.html', context)

def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You have edited your profile'))
			return redirect('home')
	else: 		#passes in user information 
		form = EditProfileForm(instance= request.user) 

	context = {'form': form}
	return render(request, 'baseapp/edit_profile.html', context)
	

def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You have edited your password'))
			return redirect('home')
	else: 		 
		form = PasswordChangeForm(user= request.user) 

	context = {'form': form}
	return render(request, 'baseapp/change_password.html', context)



#@user_passes_test(lambda u: u.is_superuser)
def create_task(request):
	#task = get_object_or_404(Task)
	if request.method =='POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, ('Task Created Successfully..'))
			return redirect('home')
	else: 		
		form = TaskForm()

	context = {'form': form}
	return render(request, 'baseapp/create_task.html',context)



@login_required
def task_detail(request):
	#user_groups = request.user.groups.all()  # Get the groups the user belongs to
	tasks = Task.objects.filter(user=request.user)
    #tasks = Task.objects.filter(assigned_to=request.user.groups.first())
	context = {
        'tasks': tasks,
    }
	
	return render(request, 'baseapp/task_list.html', context)


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'baseapp/task_edit.html', {'form': form, 'action': 'Edit'})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'baseapp/task_confirm_delete.html', {'task': task})


# @api_view(['POST'])
# def create_task_api(request):
#     if request.method == 'POST':
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def task_detail_api(request):
#     tasks = Task.objects.filter(user=request.user)
#     serializer = TaskSerializer(tasks, many=True)
#     return Response(serializer.data)


# @api_view(['PUT'])
# def task_update_api(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     serializer = TaskSerializer(task, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE'])
# def task_delete_api(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     task.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)



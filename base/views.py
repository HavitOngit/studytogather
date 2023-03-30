from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from .models import Rooms, Topic, Massage
from .form import RoomForm, UserForm
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import HttpResponse

# Create your views here.


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        # get username & password from user
        username= request.POST.get('username').lower()
        password= request.POST.get('password')

        # check is really user exits
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Not Exist')

        # Login part
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does NOT exist')


    context = {'page':page}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    #messages.success(request, 'Logout successfuly :)')
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)

            return redirect('home')
        else:
            messages.error(request, 'An error occured')
    return render(request, 'login_register.html', {'form':form})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'update-user.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    # for search
    rooms = Rooms.objects.filter(
        Q(topic__name__icontains=q) |
        Q(created__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    

    topic = Topic.objects.all()
    room_count = rooms.count()
    room_massages = Massage.objects.filter(Q(room__topic__name__icontains=q))

    return render(request, 'home.html', {'rooms':rooms, 'topics':topic, 'room_count':room_count, 'room_massages':room_massages})

def room(request, pk):
    room = Rooms.objects.get(id=pk)
    roomChat = room.massage_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        massage = Massage.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)  
    return render(request, 'room.html', {'room':room, 'roomChat':roomChat, 'participants':participants})

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.rooms_set.all()
    room_massages = user.massage_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms':rooms, 'room_massages':room_massages, 'topics':topics}
    return render(request, 'user_profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Rooms.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
        

    context = {'form': form, 'topics':topics} 
    return render(request, 'create-from.html', context) 

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Rooms.objects.get(id=pk)
    topics = Topic.objects.all()

    # by instance we get pre-filld
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here :[')
    # saving Data form user
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('room', room.id)

    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'create-from.html', context) 

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Rooms.objects.get(id=pk)
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'delete.html', {'obj':room})

@login_required(login_url='login')
def deleteChat(request, pk):
    Chat = Massage.objects.get(id=pk)
    
    if request.user != Chat.user:
        return HttpResponse('You are not allowed here :[')
    
    if request.method == 'POST':
        Chat.delete()
        return redirect('home')
    
    return render(request, 'delete.html', {'obj':Chat})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'topics_mobi.html', {'topics':topics})
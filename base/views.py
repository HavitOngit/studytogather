from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from .models import Rooms, Topic, Massage
from .form import RoomForm
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
    room_massages = Massage.objects.all()

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

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        

    context = {'form': form} 
    return render(request, 'create-from.html', context) 

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Rooms.objects.get(id=pk)

    # by instance we get pre-filld
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here :[')
    # saving Data form user
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
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
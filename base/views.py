from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from .models import Rooms, Topic
from .form import RoomForm
from django.db.models import Q
# Create your views here.


def loginPage(request):

    if request.method == 'POST':

        # get username & password from user
        username= request.POST.get('username')
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


    context = {}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    #messages.success(request, 'Logout successfuly :)')
    return redirect('home')


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

    return render(request, 'home.html', {'rooms':rooms, 'topics':topic, 'room_count':room_count})

def room(request, pk):

    context = Rooms.objects.get(id=pk)
    return render(request, 'room.html', {'room':context})


def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        

    context = {'form': form} 
    return render(request, 'create-from.html', context) 

def updateRoom(request, pk):
    room = Rooms.objects.get(id=pk)

    # by instance we get pre-filld
    form = RoomForm(instance=room)

    # saving Data form user
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'create-from.html', context) 

def deleteRoom(request, pk):
    room = Rooms.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':room})
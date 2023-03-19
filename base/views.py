from django.shortcuts import render, redirect
from .models import Rooms, Topic
from .form import RoomForm
# Create your views here.



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Rooms.objects.filter(topic__name__icontains=q)

    topic = Topic.objects.all()

    return render(request, 'home.html', {'rooms':rooms, 'topics':topic})

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
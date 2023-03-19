from django.shortcuts import render
from .models import Rooms
from .form import RoomForm
# Create your views here.


rooms = [
    {'id':1, 'name':'Python Class'},
    {'id':2, 'name':'maths Class'},
    {'id':3, 'name':'pysology Class'}
]
def home(request):
    rooms = Rooms.objects.all()
    return render(request, 'home.html', {'rooms':rooms})

def room(request, pk):
    context = Rooms.objects.get(id=pk)
    return render(request, 'room.html', {'room':context})

def createRoom(request):
    form = RoomForm()
    context = {'form': form} 
    return render(request, 'create-from.html', context) 
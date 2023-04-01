from django.forms import ModelForm
from .models import Rooms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from .models import User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Rooms
        fields = '__all__'
        # for hide speciphic field
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name','username', 'email', 'bio']
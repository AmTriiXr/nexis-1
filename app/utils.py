from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def change_password(user, new_password):
    user.set_password(new_password)
    user.save()

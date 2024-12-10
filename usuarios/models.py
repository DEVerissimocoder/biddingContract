from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
User = get_user_model()


user = User.objects.get(username='root')
user.set_password('1234')
user.save()
print("senha atualizada")



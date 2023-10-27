from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    DOB = models.DateField(null=True,blank=True)

    def __str__(self):
        return "profile {}".format(self.user.username)

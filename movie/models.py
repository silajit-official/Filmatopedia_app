from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ExtendedUser(models.Model):
    name=models.CharField(max_length=50)
    profile_pic=models.ImageField(upload_to='media')
    phone=models.IntegerField(default=0)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Group(models.Model):
    sno=models.AutoField(primary_key=True)
    admin_user=models.ForeignKey(ExtendedUser,on_delete=models.CASCADE)
    group_name=models.CharField(max_length=100)
    date=models.DateField()

    def __str__(self):
        return self.group_name


class GroupMember(models.Model):
    sno=models.AutoField(primary_key=True)
    user=models.ForeignKey(ExtendedUser,on_delete=models.CASCADE)
    group=models.ForeignKey(Group,on_delete=models.CASCADE)

    def __str__(self):
        st=f'{self.group} {self.user}'
        return st


class Suggestion(models.Model):
    sno=models.AutoField(primary_key=True)
    user=models.ForeignKey(ExtendedUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    language=models.CharField(max_length=10)
    type=models.CharField(max_length=200)
    date=models.DateField()
    req=models.IntegerField(default=5)
    group=models.ForeignKey(Group,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.title


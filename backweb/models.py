from time import timezone
from django.db import models
# from DjangoUeditor.models import UEditorField
# Create your models here.


class Typess(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'typess'




class Article(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='', null=True)
    desc = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    is_delete = models.BooleanField(default=1)
    add_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now=True)
    is_recommend = models.BooleanField(default=0)
    ty = models.ForeignKey(Typess, null=True)

    class Meta:
        db_table = 'article'





class Permission(models.Model):
    """
    权限表
    """
    p_name = models.CharField(max_length=15)
    is_delete = models.BooleanField(default=1)


    class Meta:
        db_table = 'permission'


class Role(models.Model):
    """
    角色表
    """
    r_name = models.CharField(max_length=10)
    r_p = models.ManyToManyField(Permission)
    is_delete = models.BooleanField(default=1)


    class Meta:
        db_table = 'role'





class User(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=20,null=True)
    out_time = models.DateTimeField(null=True)
    is_superuser = models.BooleanField(default=0)
    r_u = models.ForeignKey(Role, null=True)


    class Meta:
       db_table = 'users'






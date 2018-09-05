import json
from datetime import datetime, timedelta
import os
import random

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from backweb.models import Article, User, Role, Permission, Typess
from blogger import settings
from django.core.paginator import Paginator


# Create your views here.

# def login(request):
#     if request.method == 'GET':
#         return render(request,'backweb/login.html')
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         # 验证账户
#         user = auth.authenticate(request,username=username, password=password)
#         if user:
#             auth.login(request, user)
#             return HttpResponseRedirect(reverse('backweb:index'))
#         else:
#             return HttpResponseRedirect(reverse("backweb:login"))
#


# def logout(request):
#     if request.method == 'GET':
#         auth.logout(request)
#         return HttpResponseRedirect(reverse("backweb:login"))


#
# def alterw(request):
#     if request.method == 'GET':
#
#         return render(request, 'backweb/alter.html')


# 后台主页面
def index(request):
    if request.method == 'GET':
        sets = Article.objects.all()
        print(settings.STATICFILES_DIRS)
        return render(request, 'backweb/index.html')


# 文章分页预览
def pagetitle(request):
    if request.method == 'GET':
        pageid = request.GET.get('page')
        modl = request.GET.get('type')
        search = request.GET.get('search')
        if pageid is None:
            pageid = 1
        if search is None:
            search = 'None'
        if modl == None or modl == '分类':
            modl = 'all'
        # 不分类、不搜索
        if search == 'None' and modl == 'all':
            articles = Article.objects.all()
        # 搜索、不分类
        if search != 'None' and modl == 'all':
            articles = Article.objects.filter(name__icontains=search)
        # 不搜索、分类
        if search == 'None' and modl != 'all':
            articles = Article.objects.filter(ty_id=Typess.objects.get(name=modl).id)
        # 分类、搜索
        if search != 'None' and modl != 'all':
            articles = Article.objects.filter(name__icontains=search, ty_id=Typess.objects.get(name=modl).id)
        paginator = Paginator(articles, 3)
        page = paginator.page(pageid)
        types = Typess.objects.all()
        return render(request, 'backweb/pagetitle.html', {'page': page, 'types': types, 'modl': modl, 'search': search})


# 添加文章
def add(request):
    if request.method == 'GET':
        ty = Typess.objects.all()
        return render(request, 'backweb/add.html', {'ty': ty})
    if request.method == 'POST':
        title = request.POST.get('title')
        type = request.POST.get('type')
        desc = request.POST.get('desc')
        content = request.POST.get('content')
        delete = request.POST.get('delete')
        filename = request.FILES['filename']
        Article.objects.create(name=title, ty_id=type, desc=desc, image=filename, content=content, is_delete=delete)

        return HttpResponseRedirect(reverse('backweb:pagetitle/'))


# ？
def administer(request):
    if request.method == 'GET':
        return render(request, 'backweb/administer.html')


# 修改文章
def alter(request, id):
    if request.method == 'GET':
        art = Article.objects.get(id=id)
        ty = Typess.objects.all()
        return render(request, 'backweb/alter.html', {'art': art, 'ty': ty})
    if request.method == 'POST':
        art = Article.objects.get(id=id)
        art.name = request.POST.get('title')
        art.types = request.POST.get('type')
        art.desc = request.POST.get('desc')
        art.content = request.POST.get('content')
        art.is_delete = request.POST.get('delete')
        art.is_recommend = request.POST.get('recommend')
        try:
            art.image = request.FILES['filename']
        except:
            pass
        art.save()
        return pagetitle(request)


# 删除文章
def delete(request, id):
    if request.method == 'GET':
        set = Article.objects.get(id=id)
        set.delete()
        return pagetitle(request)


# 自定义注册
def my_register(request):
    if request.method == 'GET':
        return render(request, 'backweb/register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = User.objects.filter(username=username).exists()
        if user:
            error = '用户名已经储存'
            return render(request, 'backweb/register.html', {'error': error})
        else:
            if password2 == password1:
                User.objects.create(username=username, password=password2)
                return HttpResponseRedirect(reverse('backweb:my_login'))
            else:
                error = '两次密码不正确'
                return render(request, 'backweb/register.html', {'error': error})


# 自定义登录
def my_login(request, rando=None):
    if request.method == 'GET':
        return render(request, 'backweb/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 验证用户信息
        user = User.objects.filter(username=username, password=password).first()
        if user:
            # 确定跳转重定向
            res = HttpResponseRedirect(reverse('backweb:index'))
            # 写随机数字符串生成cookie
            s = 'qazwsxedcrfvtgbyhnujmikolpQZWXEDCRFVTGBYHNUJMIKOLP1234567890'
            # 给cookie定名字
            session_id = ''
            # 循环写cookie
            for i in range(20):
                session_id += random.choice(s)
            # 创建cookie过期时限默认（一天）
            out_time = datetime.now() + timedelta(days=1)
            # 为用户（服务器客户端添加）添加cookie,用来判断用户是否登录。没有登录的用户没有cookie值无法直接进
            # 入后台ides
            res.set_cookie('session_id', session_id, expires=out_time)
            user.session_id = session_id
            user.out_time = out_time
            user.save()
            # 执行跳转
            return res
        # 找不到对应数据库数据用户提供信息错误
        else:
            error = '用户名或密码错误'
            return render(request, 'backweb/login.html')


# 自定义退出
def my_logout(request):
    if request.method == 'GET':
        session_id = request.COOKIES.get('session_id')
        user = request.user
        user.session_id = ''
        user.save()

        res = HttpResponseRedirect(reverse("backweb:my_login"))
        res.delete_cookie('session_id')
        return res


# 自定义添加用户
def adduser(request):
    if request.method == 'GET':
        return render(request, 'backweb/adduser.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = User.objects.filter(username=username).exists()
        if user:
            error = '用户名已经储存'
            return render(request, 'backweb/adduser.html', {'error': error})
        else:
            if password2 == password1:
                User.objects.create(username=username, password=password2)
                return HttpResponseRedirect(reverse('backweb:my_login'))
            else:
                error = '两次密码不正确'
                return render(request, 'backweb/users.html', {'error': error})


# 点击是否展示
@csrf_exempt
def article_is_recommend(request):
    if request.method == 'POST':
        article = Article.objects.get(id=request.POST.get('id'))
        article.is_recommend = False if article.is_recommend else True
        article.save()
        res = {'A': 2}
        return HttpResponse(json.dumps(res))


# 点击是否推荐
@csrf_exempt
def article_is_delete(request):
    if request.method == 'POST':
        article = Article.objects.get(id=request.POST.get('id'))
        article.is_delete = False if article.is_delete else True
        article.save()
        resp = {'b': 2}
        return HttpResponse(json.dumps(resp))


# 添加用户与角色关系
def user_role(request):
    if request.method == 'GET':
        users = User.objects.all()
        roles = Role.objects.all()
        return render(request, 'backweb/user_role.html', {'users': users, 'roles': roles})
    if request.method == 'POST':
        username = request.POST.get('username')
        usre = User.objects.filter(username=username).first()
        role_name = request.POST.get('role_name')
        role = Role.objects.filter(r_name=role_name).first()
        usre.r_u_id = role.id
        usre.save()
        return HttpResponseRedirect(reverse("backweb:users"))


# 角色添加权限
def role_Permission(request):
    if request.method == 'GET':
        roles = Role.objects.all()
        per = Permission.objects.all()
        return render(request, 'backweb/role_Permission.html', {'per': per, 'roles': roles})
    if request.method == 'POST':
        r_name = request.POST.get('r_name')
        pers = request.POST.getlist('pers')
        role = Role.objects.filter(r_name=r_name).first()
        for per in pers:
            p = Permission.objects.filter(p_name=per).first()
            role.r_p.add(p)
        return HttpResponseRedirect(reverse("backweb:users"))


# 修改用户密码
def mod_user_password(request):
    if request.method == 'GET':
        session_id = request.COOKIES.get('session_id')
        user = User.objects.filter(session_id=session_id).first()
        return render(request, 'backweb/mod_user_password.html', {'user': user})
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        session_id = request.COOKIES.get('seeion_id')
        user = User.objects.filter(session_id=session_id).first()
        user.username = username
        pass


# 添加权限
def add_Permissio(request):
    if request.method == 'GET':
        return render(request, 'backweb/add_Permissio.html')
    if request.method == 'POST':
        name = request.POST.get('p_name')
        Permission.objects.create(p_name=name)
        return HttpResponseRedirect(reverse("backweb:users"))


# 添加权限
def add_role(request):
    if request.method == 'GET':
        return render(request, 'backweb/add_role.html')
    if request.method == 'POST':
        name = request.POST.get('r_name')
        Role.objects.create(r_name=name)
        return HttpResponseRedirect(reverse("backweb:users"))


# 用户列表
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        return render(request, 'backweb/users.html', {'users': users})

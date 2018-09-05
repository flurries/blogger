from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from backweb import views

login_required()
urlpatterns = [
    # url(r'logout/', views.logout, name='logout'),
    # url(r'alterw/', views.alterw, name='alter'),
    # url(r'login/', views.login, name='login'),

    # 后台主页面
    url(r'index/', views.index, name='index'),
    # 添加文章
    url(r'add/', views.add, name='add'),
    # ？
    url(r'administer/', views.administer, name='administer'),
    # 修改文章
    url(r'alter/(\d+)/', views.alter, name='alter/(\d+)/'),
    # 分页预览
    url(r'pagetitle/', views.pagetitle, name='pagetitle/'),
    # 删除文章
    url(r'^delete/(\d+)/$', views.delete, name='delete/(\d+)/'),
    # 自定义注册
    url(r'^my_register/', views.my_register, name='my_register'),
    # 自定义登录
    url(r'^my_login/', views.my_login, name='my_login'),
    # 自定义退出登录
    url(r'^my_logout/', views.my_logout, name='my_logout'),
    # 添加用户
    url(r'^adduser/$', views.adduser, name='addusre'),
    # 文章是否公开点击方法
    url(r'article_is_delete/', views.article_is_delete, name='article_is_delete/'),
    # 是否推荐
    url(r'article_is_recommend/', views.article_is_recommend, name='article_is_recommend/'),
    # 修改密码
    url(r'mod_user_password', views.mod_user_password, name='mod_user_password'),
    #用户列表
    url(r'users', views.users, name='users'),
    # 添加角色
    url(r'add_role', views.add_role, name='add_role'),
    #添加权限
    url(r'add_Permissio', views.add_Permissio, name='add_Permissio'),
    #添加用户的角色
    url(r'user_role', views.user_role, name='user_role'),
    #添加角色的权限
    url(r'role_Permission', views.role_Permission, name='role_Permission'),




]

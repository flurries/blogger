from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from backweb.models import Article, Typess


def index(request):
    if request.method == 'GET':
        article = Article.objects.filter(is_delete=1)[0:5]
        articles = Article.objects.filter(is_recommend=1)
        return render(request, 'web/index.html', {'article': article, 'articles': articles })


def about(request):
    if request.method == 'GET':
        return render(request, 'web/about.html')


def info(request):
    if request.method == 'GET':
        types = Typess.objects.all()
        articles = Article.objects.filter(is_recommend=1)
        return render(request, 'web/info.html', {'articles': articles, 'types': types})


def pagetitle(request):
    if request.method == 'GET':
        pageid = request.GET.get('pageid')
        rost = request.GET.get('rost')
        articles = Article.objects.filter(is_delete=1)
        types = Typess.objects.all()
        if rost == 'all':
            pass
        else:
            articles = articles.filter(ty_id=rost)
        paginator = Paginator(articles, 3)
        page = paginator.page(pageid)
        return render(request, 'web/list.html', {'types': types, 'page': page, 'rost': rost})


def searchform(request):
    if request.method == 'GET':
        pageid = request.GET.get('pageid')
        search = request.GET.get('search')
        if search == '':
            articles = Article.objects.filter(name='s1a1d')
        else:
            articles = Article.objects.filter(is_delete=1)
            articles = articles.filter(Q(name__icontains=search) | Q(content__icontains=search))
        types = Typess.objects.all()
        # 每个set页面2条数据
        paginator = Paginator(articles, 3)
        # 拿到对应页
        page = paginator.page(pageid)
        search = search
        return render(request, 'web/searchform.html', {'types': types, 'page': page, 'search': search})


def show(request, artid):
    if request.method == 'GET':
        article = Article.objects.get(id=artid)
        articles = Article.objects.filter(is_recommend=1)
        return render(request, 'web/show.html', {'article': article, 'articles': articles})


def bash(request):
    if request.method == 'GET':
        article = Article.objects.filter(is_recommend=1)
        return render(request, 'web/bash.html')



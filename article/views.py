from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import ArticleForm
from .models import Article, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def articles(request):
    keyword= request.GET.get("keyword")  #arama işlemini keywordle yaptığımız için

    if keyword:  #arama yapılarak mı gidilmiş onu kontrol ediyoruz
        articles=Article.objects.filter(title__contains =keyword)
        return render(request,"articles.html",{"articles":articles})

    articles=Article.objects.all()  #tüm articleları al

    return render(request,"articles.html",{"articles":articles})


# Ana sayfa
def index(request):
    return render(request, "index.html")

# Hakkında sayfası
def about(request):
    return render(request, "about.html")

# Kontrol paneli
@login_required(login_url="user:login")  #Giriş yapılmadıysa userın altındaki login urlsine git
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    context = {
        "articles": articles
    }
    return render(request, "dashboard.html", context)

# Makale ekle
@login_required(login_url="user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale başarıyla oluşturuldu.")
        return redirect("article:dashboard")

    return render(request, "addarticle.html", {"form": form})

# Makale detayları
def detail(request, id):
    article = get_object_or_404(Article, id=id)

    comments= article.comments.all()
    return render(request, "detail.html", {"article": article, "comments":comments})

# Makale güncelleme
@login_required(login_url="user:login")  
def updateArticle(request, id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article) #instance ile güncellenmemiş hali geliyor.

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale başarıyla güncellendi.")
        return redirect("article:dashboard")

    return render(request, "update.html", {"form": form})

#Makale Silme
@login_required(login_url="user:login")
def deleteArticle(request,id):
    article= get_object_or_404(Article,id=id)
    article.delete()
    messages.success(request,"Makale Başarıyla Silindi")

    return redirect("article:dashboard")  #articleın altındaki dashboarda git article:dashboard

def addComment(request,id):
    article= get_object_or_404(Article,id=id)

    if request.method =="POST":
        comment_author= request.POST.get("comment_author")
        comment_content= request.POST.get("comment_content")

        newComment= Comment(comment_author= comment_author, comment_content=comment_content)

        newComment.article=article

        newComment.save()
    return redirect('article:detail', id=article.id)

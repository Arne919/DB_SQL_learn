from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Article
from .forms import ArticleForm


def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'articles/index.html', context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article': article,
    }
    return render(request, 'articles/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/create.html', context)


@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        article.delete()
    return redirect('articles:index')


@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/update.html', context)


# HTML 만들때 좋아요와 관련한 if문들
# -> decorator를 안써도 된다. if문으로 다 처리해도 된다.
from django.views.decorators.http import require_POST
# 1. 로그인 되어 있어야함
@login_required
# 2. POST 요청이어야 함
@require_POST
def likes(request, pk):
    # 당연하게도, 특정 게시글을 `좋아요` 했는지를 처리한다.
    # -> 그 특정 게시글을 먼저 조회해야한다.
    article = Article.objects.get(pk=pk)
    # 게시글 좋아요 관계를 형성하거나 취소하거나 해준다.
    # if request.method == 'POST':
    #     if request.user.is_authenticated:
    # 3. 작성자 본인이어서는 안됨
    if request.user != article.user:
        # 4. 이미 좋아요를 눌렀냐 안눌렀냐에 따라서 서로 다르게 처리되어야함.
        if request.user in article.like_users.all():
            # 이미 좋아요 관계인데, 재요청 -> 삭제요청
            article.like_users.remove(request.user)
        else:
            # 아직 관계가 없는데, 요청 -> 관계 생성 요청
            article.like_users.add(request.user)

    # 로직 처리후에, POST 요청에 대한 처리는 적적한 페이지로 redirect
    return redirect('articles:index')
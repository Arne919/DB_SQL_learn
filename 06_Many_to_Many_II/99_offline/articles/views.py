from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'articles/index.html')

# def create(request):
#     return render(request, 'articles/create.html')

# def detail(request, article_pk):
#     return render(request, 'articles/detail.html')

# def update(request, article_pk):
#     return render(request, 'articles/update.html')

# def delete(request, article_pk):
#     return redirect('articles:index')

# def comment_create(request, article_pk):
#     return redirect('articles:detail', article_pk)

# def comment_delete(request, article_pk):
#     return redirect('articles:detail', article_pk)

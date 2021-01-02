from django.shortcuts import render
from .models import F3_Article


# Create your views here.

def index(request):
    articles = F3_Article.objects.filter(sorted_industrial=False)[:25]
    if request.method == "POST":
        for article in articles:
            article.sorted_industrial = True
            article.is_industrial = False
            article.save() 
        check = request.POST.getlist("is_industrial")
        for url in check:
            article = F3_Article.objects.get(url = url)
            article.is_industrial = True
            article.save()
    load_articles = F3_Article.objects.filter(sorted_industrial=False)[:25]
    return render(request, 'news_dispatcher_app/index.html', context = {"articles":load_articles, })
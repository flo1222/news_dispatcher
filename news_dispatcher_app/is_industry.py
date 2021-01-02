from dotenv import load_dotenv
load_dotenv()
import sys, os
sys.path.append("C:\\Users\\flo12\\Documents\\004_data\\news_dispatcher\\")
# print (sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','news_dispatcher.settings')
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_dispatcher.settings'
import django
django.setup()

from nltk.tokenize import word_tokenize
import csv, requests
from csv import writer, DictWriter
import re
from bs4 import BeautifulSoup
import requests
from google_trans_new import google_translator  
from news_dispatcher_app.models import Site, Article, F3_Article
from news_dispatcher_app.daily_collection import get_article_content, get_article_date, generic_article_scraping

def scrape_full_article(url):
    """A function to scrape France3 regions articles including full text"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    article = get_article_content(soup, source='France 3')
    article["url"] = url
    article["date"] = get_article_date(soup)
    paragraphs = soup.find("div", class_="article__body").find_all("p")
    full_text =''
    for paragraph in paragraphs:
        full_text = full_text + paragraph.text
    article["full_text"] = full_text[:5000]
    load_into_database(article)
    return article

def load_into_database(article):
    add_article = F3_Article(url=article["url"], image_url=article["image"],
            description=article["description"], source=article["source"],
            pub_date = article["date"], title = article["title"],
            full_text=article["full_text"])
    add_article.save()
    return None

def scrape_france3_regions_eco(start_page, end_page):
    """A function which scrapes the links and descriptions of the 
    articles of 'Economie' of France3 régions.
    The scraped content is then loaded to a database for storage."""
    for page in range(start_page, end_page +1):
        print('start page', page)
        url = f'https://france3-regions.francetvinfo.fr/economie?page={page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        link_list = []
        # Get the url of all the articles in the main page
        blocs = soup.find_all("div", class_="article-card__info")
        for bloc in blocs:
            url = bloc.find("a")["href"]
            link_list.append(url)
            # Next, scrape full content of each url
            article_list= []
        for url in link_list:
            try:
                article_list.append(scrape_full_article(url))
            except:
                print('error for:')
                print(url)
        print(f'# of articles sourced from France3region page {page} = {len(article_list)}')
    return None

def check_for_duplicates():
    count = 0
    for row in F3_Article.objects.all().order_by('-id'):
        if F3_Article.objects.filter(url=row.url).count() > 1:
            print(row.id)
            row.delete()
            count += 1
    print('#rows deleted = ', count)
    return None

def translate_article(text):
    translator = google_translator()  
    return translator.translate(text,lang_src='fr',lang_tgt='en')

def translate_F3_articles():
    articles = F3_Article.objects.all().order_by('-text_english')[:500]
    for article in articles:
        full_content = article.title + article.description + article.full_text
        article.text_english = translate_article(full_content[:4990])
        article.save()
        print(article.text_english[:100])
    return None

def character_limit_redo():
    articles = F3_Article.objects.filter(text_english__contains = 'Warning')
    for article in articles:
        full_content = article.title + article.description + article.full_text
        article.text_english = translate_article(full_content[:4950])
        article.save()
        print(article.text_english[:100])
    return None

def save_to_csv():
    # Open file in append mode
    workpath = os.path.dirname(os.path.abspath(__file__)) 
    with open(os.path.join(workpath, 'data', 'f3_region_articles.csv'), 'w', newline='',encoding="ISO 8859-1 ") as csv_file:
        # Create a writer object from csv module
        fieldnames = ['url', 'text_english', 'is_industrial']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # Add contents 
        writer.writeheader()
        articles = F3_Article.objects.all()
        for article in articles:
            writer.writerow({
                'url': article.url,
                'text_english': article.text_english.encode('ISO 8859-1', 'ignore'),
                'is_industrial':article.is_industrial
                })
    return None
           

if __name__ == "__main__":
    print('ok')
    check_for_duplicates()
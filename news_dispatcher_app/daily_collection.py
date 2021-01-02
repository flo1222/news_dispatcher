from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
load_dotenv()

import sys
# sys.path.append("C:/Users/flo12/Documents/004 - data/")
# sys.path.append("C:\\Users\\flo12\\Documents\\004 - data\\")
sys.path.append("C:\\Users\\flo12\\Documents\\004_data\\news_dispatcher\\")
# print (sys.path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_dispatcher.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE','news_dispatcher.settings')
import django
django.setup()
import datetime
import re
from selenium import webdriver
from news_dispatcher_app.models import Article, Site

# Here is a list of souces to scrape everyday for content:
sources_list = [
    'https://www.lejournaldesentreprises.com/',
    'https://france3-regions.francetvinfo.fr/economie',
    'https://actu.fr/bretagne/economie',
    'https://www.lamontagne.fr/theme/entreprendre/?page=3',
    'https://www.usinenouvelle.com/quotidien-des-usines/',
    'https://www.lesechos.fr/pme-regions',
    'https://www.ledauphine.com/economie+region/alpes+region/paca+region/vallee-du-rhone+zone/france-monde',
    'https://www.latribune.fr/regions/economie-en-region.html',
    'https://www.lavoixdunord.fr/economie',
    'https://www.leprogres.fr/economie+region/bfc-rhone-alpes+zone/france-monde',
    'https://www.ouest-france.fr/economie/entreprises/',
    'https://www.lemonde.fr/economie-francaise/'
]

# %load_ext autoreload
# %autoreload 2
def check_for_duplicates():
    count = 0
    for row in Article.objects.all().order_by('-title'):
    # for row in Article.objects.all().reverse():
    # for row in Article.objects.all():
        if Article.objects.filter(url=row.url).count() > 1:
            row.delete()
            count += 1
    print('#rows deleted = ', count)
    return None

def clean_database():
    # source = 'Ouest-France.fr'
    count = 0
    articles = Article.objects.filter(title = None)
    for article in articles:
        article.delete()
        count += 1
    print('#rows deleted = ', count)
    return None

def get_article_date(soup, source = 'default'):
    if source == 'UsineNouvelle':
        date = soup.find("time")["datetime"]
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    if source == 'LesEchos':
        date = soup.find("meta", property="article:published_time")["content"]
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+01:00')
    if source == 'Ouest-France.fr':
        date = soup.find("time")["datetime"]
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+01:00')
    else:
        date = soup.find("time")["datetime"]
        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+01:00')
    return date_time_obj

def get_article_content(soup, source = 'default'):
    article = {}
    article["image"] = soup.find("meta", property="og:image")["content"]
    article["title"] = soup.find("meta", property="og:title")["content"]
    article["description"] = soup.find("meta", property="og:description")["content"]
    article["source"] = soup.find("meta", property="og:site_name")["content"]
    if source == 'UsineNouvelle':
        article["description"] = soup.find("h2").text.strip().replace('\n', ' ').replace('\r', '')\
                .replace('\t', '').replace('   ', '')
    if source == 'France 3':
        article["description"] = soup.find("div", class_="article__chapo").text.replace('\n', ' ').strip()
    return article

def generic_article_scraping(url, source='default', delay=1):
    """This function scrapes data and description from news articles of the same
    day or the previous day, with respect to time of collection."""
    day = int(datetime.datetime.now().strftime("%d"))
    response = requests.get(url)
    print(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # article["date"] = soup.find("time")["datetime"]
    article_date = get_article_date(soup, source=source)
    date = article_date.day
    print(date)
    #Check article is 0 or 1 day old
    # if int(date) - day <= delay:
    article = get_article_content(soup, source=source)
    article["url"] = url
    article["date"] = article_date
    #Load into database
    add_article = Article(url=url, image_url=article["image"],\
            description=article["description"], source=article["source"],\
            pub_date = article["date"], title = article["title"])
    add_article.save()
    return article


def collect_usine_nouvelle():
    """A function which scrapes the links and descriptions of the 
    articles of 'Quotidien des Usines' of l'Usine Nouvelle.
    The scraped content is then loaded to a database for storage."""

    source = 'UsineNouvelle'
    # url = 'https://www.usinenouvelle.com/quotidien-des-usines/'
    url = 'https://www.usinenouvelle.com/quotidien-des-usines/5/'
    base_url = 'https://www.usinenouvelle.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    link_list = []
    # Get the url of all the articles in the main page
    blocs = soup.find_all("section", itemprop="itemListElement")
    for bloc in blocs:
        link_list.append(base_url + bloc.find("a")["href"])
    # Next, scrape the metadata of each url, as well as the description
    article_list= []
    for url in link_list:
        article_list.append(generic_article_scraping(url, source = source, delay=5))
    print(f'# of articles sourced from {source} = {len(article_list)}')
    return article_list

def collect_les_echos():
    """A function which scrapes the links and descriptions of the 
    articles of 'PME-regions' of LesEchos.
    The scraped content is then loaded to a database for storage."""

    source = 'LesEchos'
    url = 'https://www.lesechos.fr/pme-regions'
    # url = 'https://www.lesechos.fr/pme-regions?page=4'
    base_url = 'https://www.lesechos.fr'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    link_list = []
    # Get the url of all the articles in the main page
    blocs = soup.find_all("a")
    for bloc in blocs:
        url = base_url + bloc["href"]
        date = bloc.find("span")
        if 'pme-regions' in url and len(url)>50 and date:
            link_list.append(url)
    # Next, scrape the metadata of each url, as well as the description
    article_list= []
    for url in link_list:
        article_list.append(generic_article_scraping(url, source = source, delay=5))
    print(f'# of articles sourced from {source} = {len(article_list)}')
    return article_list


def collect_ouest_france():
    """A function which scrapes the links and descriptions of the 
    articles of the eco page of "Le Dauphine Libéré".
    The scraped content is then loaded to a database for storage."""

    source = "Ouest-France.fr"
    # L'url consultée est la page 2 car elle est mieux organisée que la 1.
    # Il y aura donc un delta de date de rentrée d'information
    # url = 'https://www.ouest-france.fr/economie/entreprises/'
    url = 'https://www.ouest-france.fr/economie/entreprises/?page=5'
    link_list = []
    # Selenium is needed since Ouest-France returns almost empty page from requests.
    browser = webdriver.Chrome()
    browser.get(url)
    response = browser.page_source
    browser.quit()
    #After getting the html content, we use beautiful soup to scrape
    soup = BeautifulSoup(response, "html.parser")
    # soup = BeautifulSoup(open("of2.html"), "html.parser")
    # Directly scrape the content of the page
    blocs = soup.find_all("article", class_="teaser-media clearfix") 
    article_list = []
    for bloc in blocs:
        article = {}
        article["url"] = bloc.find("a")["href"]
        image = bloc.find("img")
        # Images are lazy_loaded, so only the first 3 can be scrapped with an src attribute
        if image.has_attr("src"):
            article["image"] = image["src"]
        #The rest is scrapped looking at class lazyloaded, then searching for urls in the attribute data-oflazyload"
        #The regex search returns a list of image urls of increasing size, we take the 3rd one which is quite large.
        elif image.has_attr("data-oflazyload"):
            article["image"] = re.findall(r'(https?://[^\s]+)', image["data-oflazyload"])[2]  
        # In the meantime, a placeholder is set.
        else:
            article["image"] = 'https://www.sfi.fr/wp-content/themes/unbound/images/No-Image-Found-400x264.png'
        article["description"] = bloc.find("p").text.strip()
        article["title"] = bloc.find("h2").text.replace("bloqué", "").strip()
        print(article["title"])
        article["source"] = source
        article["date"] = get_article_date(bloc, source = source)
        article_list.append(article)
        # Load the article in the database
        add_article = Article(url=article["url"], image_url=article["image"],\
                description=article["description"], source=article["source"],\
                pub_date = article["date"], title = article["title"])
        add_article.save()
    print(f'# of articles sourced from {source} = {len(article_list)}')
    return article_list

def collect_france3region():
    """A function which scrapes the links and descriptions of the 
    articles of 'Economie' of France3 régions.
    The scraped content is then loaded to a database for storage."""

    source = 'France 3'
    url = 'https://france3-regions.francetvinfo.fr/economie'
    # url = 'https://france3-regions.francetvinfo.fr/economie?page=2'
    # base_url = 'https://www.lesechos.fr'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    link_list = []
    # Get the url of all the articles in the main page
    blocs = soup.find_all("div", class_="article-card__info")
    for bloc in blocs:
        url = bloc.find("a")["href"]
        link_list.append(url)
    # Next, scrape the metadata of each url, as well as the description
    article_list= []
    for url in link_list:
        article_list.append(generic_article_scraping(url, source = source, delay=5))
    print(f'# of articles sourced from {source} = {len(article_list)}')
    return article_list

def test():
    string_src = '&quot;offset&quot;:200,&quot;srcset&quot;:&quot;https://media.ouest-france.fr/v1/pictures/MjAyMDEyNzg3OWQ4ZDM2Y2QzNDI4ZWU3ZDBlNWI5YTJmZDdlZDk?width=320&amp;height=180&amp;focuspoint=50%2C25&amp;cropresize=1&amp;client_id=bpeditorial&amp;sign=edd5bcd3db59d354acfcaf5131e44c18e8b9d94c2146522a9c29296110b25cdc 320w,https://media.ouest-france.fr/v1/pictures/MjAyMDEyNzg3OWQ4ZDM2Y2QzNDI4ZWU3ZDBlNWI5YTJmZDdlZDk?width=375&amp;height=210&amp;focuspoint=50%2C25&amp;cropresize=1&amp;client_id=bpeditorial&amp;sign=be9fdfe9d919b0b3afe96a98d3fb2b81db8e85158815cd97f9cef533d09c0f54 375w,https://media.ouest-france.fr/v1/pictures/MjAyMDEyNzg3OWQ4ZDM2Y2QzNDI4ZWU3ZDBlNWI5YTJmZDdlZDk?width=630&amp;height=354&amp;focuspoint=50%2C25&amp;cropresize=1&amp;client_id=bpeditorial&amp;sign=6e9f95b8f54c186a2bda95eef4ca28259d69e99b9705ce8cf08c2037a6a11034 630w,https://media.ouest-france.fr/v1/pictures/MjAyMDEyNzg3OWQ4ZDM2Y2QzNDI4ZWU3ZDBlNWI5YTJmZDdlZDk?width=940&amp;height=528&amp;focuspoint=50%2C25&amp;cropresize=1&amp;client_id=bpeditorial&amp;sign=320bac4a86e8dd90f85b431677f80e539ab66bf65f9a6b00d3fef52c8c13cd09 940w&quot'
    print (re.findall(r'(https?://[^\s]+)', string_src)[2])
    return None


if __name__ == "__main__":
    print('ok')
    # test()
    collect_les_echos()
    collect_usine_nouvelle()
    collect_ouest_france()
    check_for_duplicates()
    

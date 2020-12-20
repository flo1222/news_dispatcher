from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
load_dotenv()

import sys
# sys.path.append("C:/Users/flo12/Documents/004 - data/")
# sys.path.append("C:\\Users\\flo12\\Documents\\004 - data\\")
sys.path.append("C:\\Users\\flo12\\Documents\\004 - data\\news_dispatcher\\")
# print (sys.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','news_dispatcher.settings')
import django
django.setup()
import datetime
from news_dispatcher_app.models import Article, Site

# Here is a list of souces to scrape everyday for content:
sources_list = [
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
    for row in Article.objects.all().reverse():
        if Article.objects.filter(url=row.url).count() > 1:
            row.delete()
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
    return date_time_obj

def get_article_content(soup, source = 'default'):
    article = {}
    article["image"] = soup.find("meta", property="og:image")["content"]
    article["description"] = soup.find("meta", property="og:description")["content"]
    article["source"] = soup.find("meta", property="og:site_name")["content"]
    if source == 'UsineNouvelle':
        article["description"] = soup.find("h2").text.strip().replace('\n', ' ').replace('\r', '')\
                .replace('\t', '').replace('   ', '')
    return article

def generic_article_scraping(url, source='default', delay=1):
    """This function scrapes data and description from news articles of the same
    day or the previous day, with respect to time of collection."""
    day = int(datetime.datetime.now().strftime("%d"))
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    article = {}
    # article["date"] = soup.find("time")["datetime"]
    article_date = get_article_date(soup, source=source)
    date = article_date.day
    print(date)
    #Check article is 0 or 1 day old
    if int(date) - day <= delay:
        article = get_article_content(soup, source=source)
        article["url"] = url
        article["date"] = article_date
        #Load into database
        add_article = Article(url=url, image_url=article["image"],\
                description=article["description"], source=article["source"],\
                pub_date = article["date"])
        add_article.save()
    return article


def collect_usine_nouvelle():
    """A function which scrapes the links and descriptions of the 
    articles of 'Quotidien des Usines' of l'Usine Nouvelle.
    The scraped content is then loaded to a database for storage."""

    source = 'UsineNouvelle'
    url = 'https://www.usinenouvelle.com/quotidien-des-usines/'
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
    return article_list

def collect_les_echos():
    """A function which scrapes the links and descriptions of the 
    articles of 'PME-regions' of LesEchos.
    The scraped content is then loaded to a database for storage."""

    source = 'LesEchos'
    url = 'https://www.lesechos.fr/pme-regions'
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
        print(url)
        article_list.append(generic_article_scraping(url, source = source, delay=5))
    return article_list

def test():
    return None

url = 'https://www.ledauphine.com/economie+region/alpes+region/paca+region/vallee-du-rhone+zone/france-monde'

def usine_nouvelle_content(url, delay=1):
        """This function scrapes data and description from news articles of the same
        day or the previous day, with respect to time of collection."""
        day = int(datetime.datetime.now().strftime("%d"))
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        article = {}
        article["date"] = soup.find("time")["datetime"]
        # date_time_obj = datetime.datetime.strptime(article["date"], '%Y-%m-%dT%H:%M:%S')
        date_time_obj = get_article_date(soup, source='UsineNouvelle')
        print(article["date"])
        print(date_time_obj.year)
        date = article["date"][8:10]
        #Check article is 0 or 1 day old
        if day -int(date) <= delay:
            article["url"] = url
            article["image"] = soup.find("meta", property="og:image")["content"]
            article["description"] = soup.find("h2").text.strip().replace('\n', ' ').replace('\r', '')\
                    .replace('\t', '').replace('   ', '')
            article["tag_description"] = soup.find("meta", property="og:description")["content"]
            article["source"] = soup.find("meta", property="og:site_name")["content"]
            #Load into database
            # article = Article(url=url, image_url=article["image"],\
            #         description=article["description"], source=article["source"])
            # article.save()
        return article


test_url = 'https://www.usinenouvelle.com/article/huawei-va-ouvrir-sa-premiere-usine-hors-de-chine-en-alsace.N1041774'

if __name__ == "__main__":
    # article_list = collect_usine_nouvelle()
    # print('ok')
    # for article in article_list:
    #     print(article["url"])
    #     print(article["description"])
    # collect_usine_nouvelle()
    # check_for_duplicates()
    usine_nouvelle_content(test_url)
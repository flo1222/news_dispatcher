
import csv, requests, os
from csv import writer, DictWriter

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
from nltk.tokenize import word_tokenize
import re
from news_dispatcher_app.models import Site, Article

def populate_sites():
    """A fonction that enters industrial sites from a csv file."""
    workpath = os.path.dirname(os.path.abspath(__file__)) 
    reader = open(os.path.join(workpath, 'data/industry.csv'), encoding="ISO 8859-1")
    etablissements = csv.DictReader(reader)
    counter = 0
    #Note, to reset id to 2, SELECT setval('industry_site_id_seq', 1)
    for row in etablissements:
        try:
            site = Site(name = row["nom"], siret_number = row["siret"])
            site.save()
            counter = counter + 1
        except:
            print('error')
            print(counter, row["nom"])
    return None

def populate_city_siret():
    """A fonction that add cities to each industrial site entry, from a csv file."""
    workpath = os.path.dirname(os.path.abspath(__file__)) 
    reader = open(os.path.join(workpath, 'data/industry_siret.csv'), encoding="ISO 8859-1")
    etablissements = csv.DictReader(reader)
    counter = 0
    #The first part fills siret numbers (in case of errors in the populate_site initial DB)
    for row in etablissements:
        site = Site.objects.filter(name = row["nom"])
        for item in site:
            item.siret_number = row["siret"]
            item.save()
    #The second part fills city names
            item.city = row["libelleCommuneEtablissement"]
            item.save()
    # Finally company name
            item.company = row["denominationUniteLegale"]
            item.save()    
    return None

def clean_site_duplicates():
    count = 0
    for row in Site.objects.all():
        if Site.objects.filter(siret_number=row.siret_number).count() > 1:
            print(row.name)
            row.delete()
            count += 1
    print('#rows deleted = ', count)
    return None


def match_sites():
    """A function that matches news articles with industrial sites"""
    articles = Article.objects.all()
    sites = Site.objects.all()
    for article in articles:
        article_content = article.description.lower() + article.title.lower()
        for site in sites:
            # if not site.city:
            #     print('no city for:', site.name)
            site_content = word_tokenizer(site.company)
            if site.city.lower() in article_content:
                count = 0
                for word in site_content:
                    if word in article_content and word not in site.city.lower():
                        count += 1
                        print(count, word, site.company, site.city)
                        print(article.title)
                        # article.industrial_site = site
                        # article.save()
                    elif site.company in site_content:
                        count += 1
                        print(count, word, site.company, site.city)
                        # article.industrial_site = site
                        # article.save()
    return None

def match_proba():
    articles = Article.objects.all()
    sites = Site.objects.all()
    for article in articles:
        article_content = article.description.lower() + article.title.lower()
        for site in sites:
            name = word_tokenizer(site.name)
            count = 0
            for word in name:
                if word in article_content:
                    count += 1
            if count > 1:
                print(count, site.name)
                print(article.title)
    return None
        


def word_tokenizer(content):
    stop_words = ['france', 'sas', 'le', 'la', 'les',\
         'de', 'des', 'soc', 'et', 'sa', 'du', 'pour', 'and', 'eau',\
             'production', 'solutions', 'group', 'bio',\
                 'groupe', 'transport', 'sa.']
    for word in stop_words:
        # content = content.lower().replace(word, "")
        content = re.sub(rf'\b{word}\b\s+',"",content.lower())
        content = re.sub(rf'\b{word}$',"",content)
    word_list = word_tokenize(content)
    output = []
    for word in word_list:
        if len(word)>1:
            output.append(word)
    return output


if __name__ == "__main__":
    match_sites()
    # print('ok')
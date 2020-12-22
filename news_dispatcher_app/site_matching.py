
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

def match_sites():
    """A function that matches news articles with industrial sites"""
    counter = 0
    articles = Article.objects.all()
    sites = Site.objects.all()
    for article in articles:
        description = article.description
        # for site in sites:
        if 'usine' in description:
            print(description)
            counter += 1
    print(counter)
    return None

if __name__ == "__main__":
    match_sites()
    # print('ok')
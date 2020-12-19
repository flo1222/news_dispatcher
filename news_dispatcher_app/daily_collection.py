#Database connection:
# import os
# import psycopg2
# DATABASE_URL = os.environ['DATABASE_URL']
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# conn = psycopg2.connect(
#     host="localhost",
#     database="suppliers",
#     user="postgres",
#     password="Abcd1234")

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

from bs4 import BeautifulSoup
import requests

import os
from dotenv import load_dotenv
load_dotenv()

def collect_usine_nouvelle():
    """aaa"""
    article_list= {}
    article = {}
    url = 'https://www.usinenouvelle.com/quotidien-des-usines/'
    base_url = 'https://www.usinenouvelle.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # test = soup.find_all("section", class_="colonne1")
    bloc = soup.find("section", class_="blocType1")
    article["url"] = base_url + bloc.find("a")["href"]
    
    #Next, scrape the metadata of the article_url
    response = requests.get(article["url"])
    soup = BeautifulSoup(response.content, "html.parser")
    # article["image"] = soup.find("meta", property="og:image")["content"]
    # article["description"] = soup.find("meta", property="og:description")["content"]
    # article["source"] = soup.find("meta", property="og:site_name")["content"]
    # article["url"] = url

            #    url = item.split()[0]
            # news = {}
            # response = requests.get(url)
            # soup = BeautifulSoup(response.content, "html.parser")
            # news["title"] = soup.find("meta", property="og:title")["content"]
            # news["image"] = soup.find("meta", property="og:image")["content"]
            # news["description"] = soup.find("meta", property="og:description")["content"]
            # news["source"] = soup.find("meta", property="og:site_name")["content"]
            # news["url"] = url
    return article["url"]

if __name__ == "__main__":
    print(collect_usine_nouvelle())
    print(os.getenv("SECRET_KEY"))

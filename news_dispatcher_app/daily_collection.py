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
from models import Article, Site

def collect_usine_nouvelle():
    """aaa"""
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
        article = {}
        article["url"] = url
        response = requests.get(article["url"])
        soup = BeautifulSoup(response.content, "html.parser")
        article["image"] = soup.find("meta", property="og:image")["content"]
        article["description"] = soup.find("h2").text.strip().replace('\n', ' ').replace('\r', '')\
                .replace('\t', '').replace('   ', '')
        article["tag_description"] = soup.find("meta", property="og:description")["content"]
        article["source"] = soup.find("meta", property="og:site_name")["content"]
        article_list.append(article)
        article = Article(url=url, image_url=article["image"],\
                 description=article["description"], source=article["source"])
        article.save()
    return article_list

def test():
    return None


if __name__ == "__main__":
    article_list = collect_usine_nouvelle()
    print(len(article_list))
    # for article in article_list:
    #     print(article["url"])
    #     print(article["description"])
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 23:06:45 2019

@author: p5hngk
"""

"""
Ce code permet de calculer le nombre de "bonds" entre deux urls: url_start and url_finish
Le test est ici effectué avec des pages wikipédia pour vérifier si tous les articles de la 
version anglaise de Wikipédia mènent à l'article «Philosophy». Plus précisément, 
si l'on clique sur le premier lien de chaque article, on tombera, au bout d'un moment,
sur l'article Philosophy. 
"""

import requests
from bs4 import BeautifulSoup
import urllib


def get_link(url):
    """
    Permet d'obtenir le premier lien trouver dans une page Wikipédia.
    """
    link = None

    content = requests.get(url)
    soup = BeautifulSoup(content.text, features="html.parser")
    
    #  Séléction d'un paragraphe de texte
    paragraph = soup.select("p")
    for p in paragraph:
        a = p.find("a")
        if a:
            link = a.get('href')
            break
            
    if link:
        # Reconstruction d'une url complète
        link = urllib.parse.urljoin('https://en.wikipedia.org/', link)

    return link


def go_urls(url_start, url_finish, max_iter=30):
    """
    Construction de la chaîne d'urls.
    """
    urls = []

    flag_remove_first = False
    if 'Special:Random' in url_start:
        flag_remove_first = True

    urls.append(url_start)

    while True:
        # Obtention du prochain lien à partir du dernier élément de la liste d'urls
        link = get_link(urls[-1])
        if not link:
            urls = None
            break

        urls.append(link)
        
        if urls[-1] == url_finish:
            if flag_remove_first:
                urls.pop(0) 
            print("\n Il faut {} bonds entre {} et {}".format(len(urls), urls[0], urls[-1]))
            break
        elif len(urls) > max_iter:
            if flag_remove_first:
                urls.pop(0) 
            print("\n Arrêt ! La recherche entre {} et {} est trop longue (plus de {} bonds)!".format(urls[0],
                                                                                url_finish,
                                                                                max_iter))
            break
        elif link in urls[:-1]:
            print("\n Arrêt ! La recherche tourne en boucle : deux passages sur {}".format(link))
            break
        else:
            continue
                 
    return urls


if __name__ == '__main__': 

    url_start = "https://en.wikipedia.org/wiki/Mathematics"
    url_finish = "https://en.wikipedia.org/wiki/Philosophy"
    urls = go_urls(url_start, url_finish)

    url_start = "https://en.wikipedia.org/wiki/Molecular_biophysics"
    urls = go_urls(url_start, url_finish)

    # Tests sur des urls Wikipédia aléatoires
    print("\n")
    print("\n Tests sur des URLs Wikipédia aléatoires (/wiki/Special:Random)")
    
    
    url_start = "https://en.wikipedia.org/wiki/Special:Random"
   
    for i in range(3):
        urls = go_urls(url_start, url_finish)
        
    print("\n Fin du programme ! \n")
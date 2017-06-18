
from urllib import urlopen
from bs4 import BeautifulSoup

def get_beautiful_soup_object(url):
    html = urlopen(url)
    return BeautifulSoup(html)


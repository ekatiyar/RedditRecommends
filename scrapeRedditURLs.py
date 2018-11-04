import pandas
import urllib as ul
from bs4 import BeautifulSoup, SoupStrainer
import requests
import webbrowser
def scrape(term):
    searchTerm = term
    searchUrl = "https://google.com/search?q=" + ul.parse.quote_plus(searchTerm+"reddit")
    response = requests.get(searchUrl)
    query = BeautifulSoup(response.text, "lxml")
    redditURLs = []
    for searchResult in query.find_all(class_ = "g"):
        for textWithURL in searchResult.find_all("a", href=True):
            tt = textWithURL['href']
            indexURL = tt.find("https://www.reddit")
            if indexURL != -1:
                URL = tt[indexURL:]
                redditURLs.append(URL)
    return redditURLs

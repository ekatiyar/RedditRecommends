import urllib as ul
from bs4 import BeautifulSoup
import requests

def scrape(term, modifier = "best"):
    searchTerm = term
    searchUrl = "https://google.com/search?q=" + ul.parse.quote_plus("reddit"+modifier+searchTerm)
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
    redditURLs = remove_duplicates(redditURLs)
    return redditURLs

def remove_duplicates(redditURLs):
    

print(len(scrape("earphones")))
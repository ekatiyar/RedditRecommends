import urllib as ul
from bs4 import BeautifulSoup
import requests, praw, re
from Reccomendation import reddit, CONSIDER_WIKI

def scrape(term, modifier = "best "):
    searchTerm = term
    searchUrl = "https://google.com/search?q=" + ul.parse.quote_plus("reddit "+modifier+searchTerm)
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
    dic = {}
    for url in redditURLs:
        key = submission(url)
        if key:
            dic[str(key)] = url
    return dic.values()

def submission(link):
    try:
        return reddit.submission(url=link)
    except praw.exceptions.ClientException as e:
        if "wiki" in link and CONSIDER_WIKI:
            wikiextract = re.sub(r'^(https://www.reddit.com/r/)', '', link)
            wikiextract = wikiextract.split('/wiki/')
            return reddit.subreddit(wikiextract[0]).wiki[wikiextract[1]]
        else:
            return False
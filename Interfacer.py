from scrapeRedditURLs import scrape
from Reccomendation import LinkParser
from Ranker import ranking

def search(term, modifier="best"):
    linkslist = scrape(term, modifier)
    RecDic = LinkParser(linkslist)
    return ranking(RecDic)

print(search("earphones"))
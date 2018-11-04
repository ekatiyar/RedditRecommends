from scrapeRedditURLs import scrape
from Reccomendation import LinkParser
from Ranker import ranking

def search(term, modifier="best", numitems = 10):
    linkslist = scrape(term, modifier)
    RecDic = LinkParser(linkslist)
    return ranking(RecDic, numitems)

# s = search("earphones")
# # print(len(s))
# #
# for rec in s:
#     print(rec.prod_name, rec.score, rec.link)

from Reccomendation import Recommendation, get_title

def ranking(RecDic, numitems):
    return rank_helper(remove_duplicates(RecDic), numitems)

def remove_duplicates(RecDic): # Filters list of any reoccurung links.
    Recs = RecDic.values()
    dupl = {}
    for rec in Recs:
        if rec.link in dupl:
            dupl[rec.link].append(rec)
        else:
            dupl[rec.link] = [rec]
    Recs = []
    for products in dupl.values():
        if len(products)==1:
            Recs.extend(products)
        else:
            prod = products[0]
            score = 0
            for product in products:
                score+=product.score
            Recs.extend([Recommendation(score, "", prod.link, 1, prod.prod_name)])
    return Recs

def rank_helper(listance, numitems): # Ranks products according to score.
    s_listance = sorted(listance, key = lambda rec: rec.score, reverse=True)[:numitems]
    for instance in s_listance[:]:
        title = get_title(instance)
        if title:
            instance.prod_name = title
        else:
            s_listance.remove(instance)
    return s_listance
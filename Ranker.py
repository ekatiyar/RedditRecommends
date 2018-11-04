from Reccomendation import LinkParser, Recommendation

def ranking(RecDic):
    return rank_helper(remove_duplicates(RecDic))

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
            Recs.extend([Recommendation(prod.prod_name, score, "", prod.link, 1)])
    return Recs

def rank_helper(listance): # Ranks products according to score.
    return sorted(listance, key = lambda rec: rec.score, reverse=True)

# links = ["https://www.reddit.com/r/MechanicalKeyboards/comments/7js58d/what_mechanical_keyboard_should_i_buy/",
#          "https://www.reddit.com/r/MechanicalKeyboards/comments/8ekjay/best_mechanical_keyboard_100200/",
#          "https://www.reddit.com/r/MechanicalKeyboards/comments/8lk5nh/mechanical_keyboard_suggestions/"]
#
# reccs = LinkParser(links)
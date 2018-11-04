import praw, requests, re, os
from bs4 import BeautifulSoup

reddit = praw.Reddit(client_id=os.environ.get('rclientid'),
                     client_secret=os.environ.get('rclientsecret'),
                     user_agent=os.environ.get('useragent'))
URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
WEBFILTER = ['reddit', 'gfycat', 'imgur', '.jpg', '.png']
WIKI_SCORE = 5
CONSIDER_WIKI=True
SUB_DIVISOR = 10

class Recommendation:
    def __init__(self, score, text, link, sentiment = 1, prod_name = None):
        self.prod_name = prod_name
        self.score = score*sentiment
        self.text = text
        self.link = link
        self.sentiment = sentiment

    def __hash__(self):
        return hash(str(self.link+self.text[:61]))

    def modify_sentiment(self, newsent):
        self.score*=newsent/self.sentiment

def title_filter(prod_name):
    if "amazon.com" in prod_name.lower():
        return prod_name.split(': ')[1]
    else:
        return re.sub(r"(\|.*$)", '', prod_name)

def text_parse(text, score):
    Recommendations = []
    links = [link for link in re.findall(URL_REGEX, text) if all(term not in link.lower() for term in WEBFILTER) and "http" in link]
    for link in links:
        Recommendations.append(Recommendation(score, text, link))
    return Recommendations

def LinkParser(linkslist):
    Recommendations = []
    for link in linkslist:
        try:
            sub = reddit.submission(url=link)
            Recommendations.extend(text_parse(sub.selftext, sub.score//SUB_DIVISOR))
            #sub.comments.replace_more(limit=None)
            for comment in sub.comments.list():
                if isinstance(comment, praw.models.reddit.comment.Comment):
                    Recommendations.extend(text_parse(comment.body, comment.score))
        except praw.exceptions.ClientException as e:
            if "wiki" in link and CONSIDER_WIKI:
                wikiextract = re.sub(r'^(https://www.reddit.com/r/)', '', link)
                wikiextract = wikiextract.split('/wiki/')
                text = reddit.subreddit(wikiextract[0]).wiki[wikiextract[1]].content_md
                Recommendations.extend(text_parse(text, WIKI_SCORE))
            else:
                print(e)
    RecDic = {hash(r): r for r in Recommendations}
    return RecDic

def get_title(instance):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    req = requests.get(instance.link, headers=headers).text
    soup = BeautifulSoup(requests.get(instance.link).content, features="html.parser")
    if soup.title:
        return title_filter(soup.title.string)
import praw

reddit = praw.Reddit('RedditRecommends')

class Recomend:
    def __init__(self, submission):
        self.text = submission.selftext if isinstance(submission, praw.models.Submission) else submission.body
        self.score = submission.score

    def __str__(self):
        return self.text + ", " + str(self.score)

class Post(Recomend):
    def __init__(self, submission):
        self.sentiment = 1
        self.children = [Comment(self, comm) for comm in submission.comments]
        super().__init__(submission)

    def __str__(self):
        return super().__str__() + '\n' + '\n'.join([str(child) for child in self.children])

class Comment(Recomend):
    def __init__(self, parent, comment):
        self.parent = parent
        super().__init__(comment)

def LinksParser(linkslist):
    return [Post(reddit.submission(url=link)) for link in linkslist]
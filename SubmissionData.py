import praw

reddit = praw.Reddit('RedditRecommends')

print(reddit.read_only)

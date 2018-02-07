import praw
import pprint

reddit = praw.Reddit('owbot', user_agent='owbot user agent')

reply_template = 'A Blizzard employee has replied to this topic. You can read their responses here:\n\n*{}'

subreddit = reddit.subreddit('overwatchcss')

for comment in subreddit.stream.comments():
    if "blizztest" in str(comment.author_flair_css_class) and comment.created > 1518018589:
        print(comment.link_id)
        parent = comment.link_id.split('_')[1]
        reddit.submission(parent).reply("I found a blue post!")

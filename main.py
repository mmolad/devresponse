# initialize libraries
import praw
import pprint
import os
#start up the bot. enter your bot name as defined in your praw ini file
reddit = praw.Reddit('owbot', user_agent='owbot user agent')

# define which subreddit we're working in.
subreddit = reddit.subreddit('overwatchcss')

# this is how we start each post
reply_template = '**A Blizzard employee has replied to this topic. You can read their responses here:**\n\n1. '

# track the ones we've already replied to in a CSV file.  let's move this to SQL later.
if not os.path.isfile("tracked_submissions.csv"):
    tracked_submissions = []
else:
    with open("tracked_submissions.csv", "r") as f:
        tracked_submissions = f.read()
        tracked_submissions = tracked_submissions.split("\r\n")
        tracked_submissions = list(filter(None, tracked_submissions))

# iterate on all comments as they come in
for comment in subreddit.stream.comments():
    
    id = comment.id
    
    # check for flair, and future timestamp
    if "blizztest" in str(comment.author_flair_css_class) and comment.created > 1518018589:
        
        
        # truncate the submission, if it is under 25 characters, print as-is
        body = comment.body
        
        if len(body) >= 25:
            brief = body[:25] + "..."
        else: 
            brief = body
        
        # find the submission ID
        parent = comment.link_id.split('_')[1]

        # check if we've already tracked this parent
        if parent not in tracked_submissions:
            print("New submission found: " + parent)
            
            # add our reply
            reply_text = reply_template + "**/u/" + str(comment.author) + "**: [" + str(brief) + "](" + comment.permalink + ")"

            reddit.submission(parent).reply(reply_text).mod.distinguish(sticky=True)

            # store the parent and comment id in our list
            tracked_submissions.append(parent + "," + comment.id)

            # also update our CSV
            with open("tracked_submissions.csv", "w") as f:
                f.write(parent + "\r\n")
        else

            # check if the specific comment has been tracked
            if id not in tracked_submissions:
                

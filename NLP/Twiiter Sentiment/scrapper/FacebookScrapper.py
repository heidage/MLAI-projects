from facebook_scraper import get_posts

for post in get_posts('nike', pages=1):
    print(post['text'])
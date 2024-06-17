import discord
from discord.ext import tasks
import feedparser

# Specify intents for the bot
intents = discord.Intents.default()
intents.messages = True  # Enable if your bot needs to read messages
intents.guilds = True    # Enable if your bot needs to interact with guilds

# Discord bot token - Replace 'your_actual_bot_token_here' with your bot's token
BOT_TOKEN = 'MTIyMTU1Nzk5MzA5NTY5NjUxNQ.GF_Ujd.jVTZrXL9iR-u8cQ42sN5tC5svfsI58mHdJwg6I'

# Discord channel ID where messages will be sent
CHANNEL_ID = 1210330503098667109

# List of RSS feed URLs to monitor
RSS_FEED_URLS = [
    'https://tldr.tech/api/rss/tech',
    'http://feeds.feedburner.com/TechCrunch/',
    'https://techcrunch.com/feed/',
    'https://www.artificialintelligence-news.com/feed/',
    'https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml',
    'https://news.mit.edu/rss/topic/artificial-intelligence-machine-learning',
    'https://news.mit.edu/rss/topic/robotics',
    'https://news.mit.edu/rss/topic/algorithms',
    'https://news.mit.edu/rss/topic/computing',
    'https://news.mit.edu/rss/topic/human-computer-interaction',
    'https://news.mit.edu/rss/topic/computer-science',
    'https://news.mit.edu/rss/topic/history-science',
    'https://news.mit.edu/rss/topic/quantum-computing',
    'https://techmeme.com/feed.xml',  # Techmeme: Essential tech news
    'https://feeds.arstechnica.com/arstechnica/index',  # Ars Technica: News and reviews
    'https://engadget.com/rss.xml',  # Engadget: Consumer tech news and reviews
    'https://theverge.com/rss/index.xml',  # The Verge: Technology, science, art, and culture
    'https://androidauthority.com/feed',  # Android Authority: Android news, reviews, and tips
    'https://pcworld.com/index.rss',  # PCWorld: News, tips and reviews on PCs, Windows, and more
    'https://feeds.feedburner.com/thenextweb',  # The Next Web: Internet technology, business and culture
    # Cannabis-related RSS feeds
    'https://www.cannabisindustryjournal.com/feed/',  # Cannabis Industry Journal: Quality, Regulatory, Operations, Business Analysis
    'https://420intel.com/rss',  # 420 Intel: Cannabis Legalization and Technology News
    'https://www.leafly.com/news/rss',  # Leafly: Cannabis Strain and Dispensary News
    'https://mjbizdaily.com/feed/',  # MJBizDaily: U.S. Cannabis Business News
    'https://www.marijuanamoment.net/feed/',  # Marijuana Moment: Cannabis Policy, Science, and Culture
    'https://stackoverflow.blog/feed/atom/',
    'http://feeds.feedburner.com/ServeTheHome',
    'https://adamtheautomator.com/feed/',
    'https://4sysops.com/feed/',
    'https://singularityhub.com/tag/artificial-intelligence/',
    'https://techxplore.com/machine-learning-ai-news/',
    'https://slashdot.org/search/ai',
    'https://dev.to/feed/'
    # Add more RSS feed URLs as needed
]

# Time interval in seconds for checking the feeds
CHECK_INTERVAL = 300

# Keep track of the latest post published for each feed
latest_posts = {feed_url: '' for feed_url in RSS_FEED_URLS}

# Initialize the client with the specified intents
client = discord.Client(intents=intents)

@tasks.loop(seconds=CHECK_INTERVAL)
async def check_feeds():
    for feed_url in RSS_FEED_URLS:
        feed = feedparser.parse(feed_url)
        if feed.entries:
            newest_post = feed.entries[0]
            # Check if 'id' attribute exists, fallback to 'link' if not
            post_id = newest_post.get('id', newest_post.link)  # Modified line
            if latest_posts[feed_url] == '' or post_id != latest_posts[feed_url]:
                # Handle first run or new post
                channel = client.get_channel(CHANNEL_ID)
                if channel:  # Check if the channel was found
                    await channel.send(f"**{newest_post.title}**\n{newest_post.link}")
                    latest_posts[feed_url] = post_id  # Modified line
                else:
                    print(f"Could not find channel with ID {CHANNEL_ID}")
            else:
                print("No new posts to publish for feed:", feed_url)
        else:
            print("No entries found in feed:", feed_url)


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    check_feeds.start()  # Start the task to check the feeds

client.run(BOT_TOKEN)
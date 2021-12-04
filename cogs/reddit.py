import discord, random, praw, os

from discord.ext import commands
from boot.meifwa import MeifwaBot


class Reddit(commands.Cog):
    def __init__(self, client: MeifwaBot):
        self.client = client
    
    @commands.command(aliases = ['r', 'reddi', 'redd', 'red', 're'])
    @commands.cooldown(3, 30, commands.BucketType.channel)
    async def reddit(self, ctx, subreddit):
        r = praw.Reddit(client_id="myVr7vToLuADLQLCMBrfpQ",
        client_secret=self.client.get_config("config", "config", "reddit_secret"),
        user_agent="meifwa")

        print(f"{ctx.guild.name} - #{ctx.channel.name} - {ctx.author.name} - {ctx.message.content}")
        submissions = []
        def check_subreddit(subreddit):
            valid = True
            if subreddit == 'all' or subreddit == 'popular':
                return valid
            try:
                r.subreddit(subreddit).subreddit_type
            except:
                valid = False
            return valid
        if not check_subreddit(subreddit):
            await ctx.send("Invalid subreddit.")
            return
        for submission in r.subreddit(subreddit).hot(limit=50):
            submissions.append(submission)
        submission = submissions[random.randint(0, len(submissions) - 1)]
        embed = discord.Embed(
            description = f"[{submission.title}](https://reddit.com{submission.permalink})",
            title = f"r/{subreddit}",
            color=ctx.message.author.color,
            timestamp=ctx.message.created_at
        )
        embed.set_author(name="Requested By: " + str(ctx.message.author), icon_url=ctx.message.author.avatar.url)
        embed.set_footer(text = f"{submission.score} points | {submission.num_comments} comments")
        if submission.is_self:
            embed.description += f"\n\n{submission.selftext}"
            await ctx.send(embed = embed)
            return
        if submission.over_18 and not ctx.channel.is_nsfw():
            await ctx.send("NSFW commands can only be used in a NSFW channel.")
            return
        if submission.url.startswith('https://i.redd.it/'):
            embed.set_image(url = submission.url)
            await ctx.send(embed = embed)
        elif submission.url.startswith('https://v.redd.it/'):
            await ctx.send(submission.url)
        elif submission.url.startswith('/r/'):
            embed.description += f"\n\nhttps://reddit.com{submission.url}"
            await ctx.send(embed = embed)
        else:
            await ctx.send(embed = embed)
            await ctx.send(submission.url)
    
    @reddit.error
    async def reddit_error(self, ctx, error):
        print(error)
        await ctx.send("Please follow format: `y.reddit {subreddit}`")
    
def setup(client):
    client.add_cog(Reddit(client))
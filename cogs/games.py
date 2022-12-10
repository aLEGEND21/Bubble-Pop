import discord
from discord import option
from balloon_pop import BalloonPop


class Games(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    @discord.Cog.listener()
    async def on_ready(self):
        print("cogs.games is online")
        
    @discord.slash_command()
    @option("bet", description="How much you want to bet", type=int)
    async def balloon_pop(self, ctx: discord.ApplicationContext, bet: int):
        await ctx.defer()
        
        if bet < 1:
            return await ctx.respond("You can't bet less than 1")
        
        game = BalloonPop(self.bot, self, ctx, bet)
        await game.start_game()
        

def setup(bot):
    bot.add_cog(Games(bot))
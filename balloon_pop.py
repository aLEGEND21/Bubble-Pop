import discord
from discord.ui import View, Button

import random


#config panel [danger]

RED_CHANCE = 0.25
BLUE_CHANCE = 0.33
GREEN_CHANCE = 0.5

RED_MULTIPLIER = 0.5
BLUE_MULTIPLIER = 1
GREEN_MULTIPLIER = 2

RED_BALLOON_EMOJI = "🟥"
BLUE_BALLOON_EMOJI = "🟦"
GREEN_BALLOON_EMOJI = "🟩"

#config panel [danger]


class BalloonPop:
    def __init__(self, bot: discord.Bot, cog: discord.Cog, ctx: discord.ApplicationContext, bet: int):
        self.bot = bot
        self.cog = cog
        self.ctx = ctx
        self.bet = bet
        
        self.embed: discord.Embed = None
        self.view: View = None
        self.multiplier: float = 0.0
        self.payout: float = 0.0
        self.running: bool = True
        self.win_type: int = None
    
    async def start_game(self):
        """Starts the game and sends the first message.
        """
        await self.update_embed()
        await self.update_view()
        await self.ctx.respond(embeds=[self.embed], view=self.view)
    
    async def update_message(self, interaction: discord.Interaction = None):
        """Updates the message with the new embed and view through the context.
        """
        await self.update_embed()
        await self.update_view()
        if interaction is not None:
            await interaction.response.edit_message(embeds=[self.embed], view=self.view)
        else:
            await self.ctx.edit(embeds=[self.embed], view=self.view)
    
    async def update_embed(self):
        """Creates the embed for the game and stores it in self.embed.
        """
        if self.running:
            self.embed = discord.Embed(
                title="Playing [Balloon Pop]",
                description=f"`Multiplier: {self.multiplier}x`\n**Bet**\n`${self.bet}`\n**Payout**\n`${self.payout}`",
                color=discord.Color.blurple()
            )
        else:
            self.embed = discord.Embed(
                title="Game Over [Balloon Pop]",
                description=f"`Multiplier: {self.multiplier}x`\n**Bet**\n`${self.bet}`\n**Payout**\n`${self.payout}`",
                color=discord.Color.blurple()
            )
        
    async def update_view(self):
        """Creates the view for the game and stores it in self.view.
        """
        red = Button(emoji=RED_BALLOON_EMOJI, style=discord.ButtonStyle.blurple, custom_id="red")
        blue = Button(emoji=BLUE_BALLOON_EMOJI, style=discord.ButtonStyle.blurple, custom_id="blue")
        green = Button(emoji=GREEN_BALLOON_EMOJI, style=discord.ButtonStyle.blurple, custom_id="green")
        stop = Button(label="Stop", style=discord.ButtonStyle.danger, custom_id="stop")
        red.callback = self.on_button_click
        blue.callback = self.on_button_click
        green.callback = self.on_button_click
        stop.callback = self.on_button_click
        self.view = View(red, blue, green, stop)
        self.view.on_timeout = self.on_timeout
        
        if not self.running:
            self.view.clear_items()
    
    async def on_button_click(self, interaction: discord.Interaction):
        """Handles the button clicks.
        """
        if interaction.user != self.ctx.author:
            return await interaction.response.send_message(":x: You can't play this game", ephemeral=True)
        
        if interaction.custom_id == "stop":
            #await interaction.response.send_message(":x: You stopped the game", ephemeral=True)
            self.win_type = 1
            await self.game_over(interaction)
        
        elif interaction.custom_id == "red":
            if random.random() > RED_CHANCE:
                self.multiplier += RED_MULTIPLIER
                self.payout = self.bet * self.multiplier
                #await interaction.response.send_message(f":white_check_mark: The {RED_BALLOON_EMOJI} red balloon didn't pop", ephemeral=True)
                await self.update_message(interaction)
            else:
                #await interaction.response.send_message(f":x: You popped the {RED_BALLOON_EMOJI} red balloon and lost", ephemeral=True)
                self.win_type = 0
                await self.game_over(interaction)
        
        elif interaction.custom_id == "blue":
            if random.random() > BLUE_CHANCE:
                self.multiplier += BLUE_MULTIPLIER
                self.payout = self.bet * self.multiplier
                #await interaction.response.send_message(f":white_check_mark: The {BLUE_BALLOON_EMOJI} blue balloon didn't pop", ephemeral=True)
                await self.update_message(interaction)
            else:
                #await interaction.response.send_message(f":x: You popped the {BLUE_BALLOON_EMOJI} blue balloon and lost", ephemeral=True)
                self.win_type = 0
                await self.game_over(interaction)
        
        elif interaction.custom_id == "green":
            if random.random() > GREEN_CHANCE:
                self.multiplier += GREEN_MULTIPLIER
                self.payout = self.bet * self.multiplier
                #await interaction.response.send_message(f":white_check_mark: The {GREEN_BALLOON_EMOJI} green balloon didn't pop", ephemeral=True)
                await self.update_message(interaction)
            else:
                #await interaction.response.send_message(f":x: You popped the {GREEN_BALLOON_EMOJI} green balloon and lost", ephemeral=True)
                self.win_type = 0
                await self.game_over(interaction)
    
    async def on_timeout(self):
        """Triggers the game over method when the view times out.
        """
        await self.game_over()
    
    async def game_over(self, interaction: discord.Interaction = None):
        """Is called when the game is over. It stops the game and updates the message. Any cleanup should be done here.
        """
        self.running = False
        if self.win_type == 0:
            self.multiplier = 0.0
            self.payout = 0.0
        await self.update_message(interaction)
        
        
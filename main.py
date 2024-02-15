from discord.ext import commands
import discord
import os
import asyncio
from embed import *

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

prefix = "c"

bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

embed = discord.Embed(title='Commands',
                          color=discord.Color.blue())

# Load the cog
async def load_cogs():
    await bot.load_extension("tts")


@bot.event
async def on_ready():
    bot.loop.create_task(bot.change_presence(activity=discord.Game(name=f"{prefix}commands")))
    print(f"Bot is ready! {bot.user.name}")


@bot.command(name = 'commands', aliases = ['c'])
async def commands(ctx):
    '''
    Show list of commands
    '''
    await ctx.send(embed=embed_commands(prefix, bot, embed))

async def main():
    await load_cogs()

asyncio.run(main())
bot.run(os.getenv('TTOKEN'))

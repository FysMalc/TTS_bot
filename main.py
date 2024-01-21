from discord.ext import commands
import discord
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

prefix = "c!"

bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)


# Load the cog
async def load_cogs():
    await bot.load_extension("tts")


@bot.event
async def on_ready():
    print(f"Bot is ready! {bot.user.name}")

@bot.command()
async def commands(ctx):
    embed = discord.Embed(title='Help',
                          description='Danh sách lệnh',
                          color=discord.Color.dark_embed())
    embed.add_field(name=f"{prefix}join",
                    value="Bot vào kênh của bạn",
                    inline=False)
    embed.add_field(name=f"{prefix}leave",
                    value="Bot ra khỏi kênh",
                    inline=False)
    embed.add_field(name=f"{prefix}s [text]",
                    value="Bot nói [text]",
                    inline=False)
    embed.add_field(name=f"{prefix}stop ", value="Dừng bot", inline=True)
    embed.add_field(name=f"{prefix}lang [language]",
                    value="Bot sẽ dùng giọng [language] để nói",
                    inline=False)
    embed.add_field(name=f"{prefix}llist",
                    value="Hiển thị danh sách các ngôn ngữ hỗ trợ",
                    inline=False)
    embed.add_field(name=f"{prefix}commands",
                    value="Hiển thị danh sách các lệnh",
                    inline=False)
    embed.add_field(name=f"{prefix}fb [phản hồi]",
                    value="Gửi phản hồi cho Nem những thứ bạn muốn thêm hay bỏ",
                    inline=False)
    embed.add_field(name=f"{prefix}outro", value="Chơi outro", inline=False)
    await ctx.send(embed=embed)

async def main():
    await load_cogs()


asyncio.run(main())
bot.run("TOKEN")

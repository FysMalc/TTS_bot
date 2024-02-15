
from discord.ext import commands
import discord
import gtts
import asyncio
import re
from datetime import datetime
from utils import *
from constants import *
from embed import *

class TTS(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.server_data = {}
        self.lang_dict = LANG_DICT

        self.timezone = TIME_ZONE

    @commands.command(name = 'join', aliases = ['j'])
    async def join(self, ctx):
        '''
        Join voice channel
        '''
        if not (author_voice := ctx.author.voice):
            await ctx.send("Ủa vào room chưa zị.")
            return
        
        await ensure_voice_client(ctx.guild, author_voice.channel, self.server_data)

    @commands.command(name = 'languagelist', aliases = ['llist', 'll'])
    async def llist(self, ctx):
        '''
        List available languages
        '''
        await ctx.send(embed = embed_llist(self.lang_dict))

    @commands.command(name = 'lang', aliases = ['la'])
    async def lang(self, ctx, lang):
        '''
        Set bot's language
        '''
        guild_id = ctx.guild.id
        self.server_data[guild_id]["default_lang"] = lang
        await ctx.send(f"Đã chuyển sang giọng {self.lang_dict[lang]}")

    @commands.command(name = 'say', aliases = ['speak', 's'])
    async def say(self, ctx, *, text):
        '''
        Say something
        '''
        time = datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S')

        guild_id = ctx.guild.id
        if guild_id not in self.server_data:
            await ctx.send(
                "Cho em join room đi đã em mới nói được. Nhập `c!join`")
            return

        voice_client = self.server_data[guild_id]["voice_client"]
        is_bot_in_use = self.server_data[guild_id]["is_bot_in_use"]
        lang = self.server_data[guild_id]["default_lang"]

        if is_bot_in_use:
            self.server_data[guild_id]["message_queue"].append(text)
            return
        
        self.server_data[guild_id]["is_bot_in_use"] = True

        if re.search(SMILEY_REGEX, text):
            text = re.sub(SMILEY_REGEX, "mặt cười", text)
        elif re.search(FROWN_REGEX, text):
            text = re.sub(FROWN_REGEX, "mặt buồn", text)

        try:
            tts = gtts.gTTS(text=text, lang=lang, slow=False)

            # Save the TTS to a file
            tts.save(f'tts/tts_{guild_id}.wav')
            
            voice_client.play(
                discord.FFmpegPCMAudio(f"tts/tts_{guild_id}.wav",
                                       executable="ffmpeg"))

            # Wait for the TTS to finish playing
            while voice_client.is_playing():
                await asyncio.sleep(1)

        except Exception as e:
            with open("error.txt", "a", encoding='utf-8') as f:
                f.write(f"[{time}] {ctx.author.name} {text}: lỗi {e}\n")

        self.server_data[guild_id]["is_bot_in_use"] = False
        if self.server_data[guild_id]["message_queue"]:
            next_text = self.server_data[guild_id]["message_queue"].pop(0)
            await self.s(ctx, text=next_text)

    @commands.command(name = 'leave', aliases = ['l'])
    async def leave(self, ctx):
        '''
        Leave voice channel
        '''
        guild_id = ctx.guild.id
        if guild_id in self.server_data and self.server_data[guild_id][
                "voice_client"]:
            await self.server_data[guild_id]["voice_client"].disconnect()
            self.server_data.pop(guild_id)

    @commands.command(name = 'outro')
    async def outro(self, ctx):
        '''
        Bot plays outro
        '''
        await self.join(ctx)

        guild_id = ctx.guild.id
        voice_client = self.server_data[guild_id]['voice_client']
        if self.server_data[guild_id]["is_bot_in_use"]:
            await ctx.send("Đợi em nói xong đã rồi thử lại nha.")
            return

        self.server_data[guild_id]["is_bot_in_use"] = True
        voice_client.play(
            discord.FFmpegPCMAudio("sound/outro.mp3", executable="ffmpeg"))

        while voice_client.is_playing():
            await asyncio.sleep(1)

        self.server_data[guild_id]["is_bot_in_use"] = False

    @commands.command(name = 'stop')
    async def stop(self, ctx):
        '''
        Stop playing
        '''
        if self.server_data[ctx.guild.id]['voice_client'].is_playing():
            self.server_data[ctx.guild.id]['voice_client'].stop()

    @commands.command(name = 'feedback', aliases = ['fb'])
    async def fb(self, ctx, *, text = None):
        '''
        Give feedback for author
        '''
        if not text:
            await ctx.send("missing feedback")
            return
        
        time = datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S')

        with open("feedback.txt", "a") as f:
            f.write(f"[{time}] {ctx.guild.name} {ctx.author.name}: {text}\n")
        await ctx.send("Nem sẽ xem feedback khi Nem dệy nha :3")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog '{self.__class__.__name__}' is ready!")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Check if the bot is in a voice channel on the same server
        guild_id = member.guild.id
        if guild_id in self.server_data and self.server_data[guild_id]["voice_client"]:
            # Check if all members are disconnected
            all_members_disconnected = all(m.bot or m.voice is None for m in member.guild.members)

            if all_members_disconnected:
                # Schedule disconnection after 10 seconds
                await asyncio.sleep(180)
                # Check again to ensure no one has joined during the delay
                if all(m.bot or m.voice is None for m in member.guild.members):
                    await self.server_data[guild_id]["voice_client"].disconnect()
                    self.server_data.pop(guild_id)

async def setup(bot):
    await bot.add_cog(TTS(bot))

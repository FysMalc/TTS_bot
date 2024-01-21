from sys import executable
from discord import voice_client
from discord.ext import commands
import discord
import gtts
import asyncio
import re
from datetime import datetime
import pytz


class TTS(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.server_data = {}
        self.lang_dict = {
            "vi": "vietnamese",
            "en": "english",
            "fr": "french",
            "es": "spanish",
            "de": "german",
            "it": "italian",
            "ja": "japanese",
            "ko": "korean",
            "tl": "philippines",
            "zh": "chinese",
        }
        self.smiley_regex = r':[)]+'
        self.frown_regex = r":[(]+"
        self.timezone = pytz.timezone("Asia/Ho_Chi_Minh")
        self.embed = discord.Embed(title='Language list',
                                   color=discord.Color.dark_embed())

    @commands.command()
    async def join(self, ctx):
        '''
        Join voice channel
        '''

        guild_id = ctx.guild.id
        if guild_id not in self.server_data:
            self.server_data[guild_id] = {
                "voice_client": None,
                "is_bot_in_use": None,
                "default_lang": "vi",
                "message_queue": []
            }
        await ctx.send(
            "Dùng lệnh `!fb [phản hồi]` để gửi phản hồi lại cho Nem nha.")
        if self.server_data[guild_id]["voice_client"]:
            await self.server_data[guild_id]["voice_client"].disconnect()

        channel = ctx.author.voice.channel
        self.server_data[guild_id]["voice_client"] = await channel.connect()

        self.voice = self.server_data[guild_id]["voice_client"]
        tts = gtts.gTTS(self.get_message(),
                        lang=self.server_data[guild_id]["default_lang"])
        tts.save(f"tts_{guild_id}.mp3")
        self.voice.play(
            discord.FFmpegPCMAudio(f"tts_{guild_id}.mp3", executable="ffmpeg"))

    @commands.command()
    async def llist(self, ctx):
        '''
        List available languages
        '''
        for i in self.lang_dict:
            self.embed.add_field(name= f"{i}: {self.lang_dict[i]}", value = "", inline=False)
        await ctx.send(embed = self.embed)

    @commands.command()
    async def lang(self, ctx, lang):
        '''
        Set bot's language
        '''

        guild_id = ctx.guild.id
        self.server_data[guild_id]["default_lang"] = lang
        await ctx.send(f"Đã chuyển sang giọng {self.lang_dict[lang]}")

    @commands.command()
    async def s(self, ctx, *, text):
        '''
        Say something
        '''

        time = datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S')

        guild_id = ctx.guild.id
        if guild_id not in self.server_data:
            await ctx.send(
                "Cho em join room đi đã em mới nói được. Nhập `!join`")
            return

        self.voice = self.server_data[guild_id]["voice_client"]
        is_bot_in_use = self.server_data[guild_id]["is_bot_in_use"]
        lang = self.server_data[guild_id]["default_lang"]

        if is_bot_in_use:
            self.server_data[guild_id]["message_queue"].append(text)
            return
        else:
            self.server_data[guild_id]["is_bot_in_use"] = True

        if re.search(self.smiley_regex, text):
            text = re.sub(self.smiley_regex, "mặt cười", text)
        elif re.search(self.frown_regex, text):
            text = re.sub(self.frown_regex, "mặt buồn", text)

        try:
            tts = gtts.gTTS(text=text, lang=lang, slow=False)

            # Save the TTS to a file
            tts.save(f'tts_{guild_id}.mp3')

            self.voice.play(
                discord.FFmpegPCMAudio(f'tts_{guild_id}.mp3',
                                       executable="ffmpeg"))

            # Wait for the TTS to finish playing
            while self.voice.is_playing():
                await asyncio.sleep(1)
        except Exception as e:
            with open("error.txt", "a") as f:
                f.write(f"{time} {text}: lỗi {e}\n")

        self.server_data[guild_id]["is_bot_in_use"] = False
        if self.server_data[guild_id]["message_queue"]:
            next_text = self.server_data[guild_id]["message_queue"].pop(0)
            await self.s(ctx, text=next_text)

    @commands.command()
    async def leave(self, ctx):
        '''
        Leave voice channel
        '''

        guild_id = ctx.guild.id
        if guild_id in self.server_data and self.server_data[guild_id][
                "voice_client"]:
            await self.server_data[guild_id]["voice_client"].disconnect()
            self.server_data.pop(guild_id)

    @commands.command()
    async def outro(self, ctx):
        '''
        Bot plays outro
        '''

        guild_id = ctx.guild.id
        if guild_id not in self.server_data:
            await ctx.send(
                "Cho em join room đi đã em mới chơi outro được. Nhập `!join`")

        if self.server_data[guild_id]["is_bot_in_use"]:
            ctx.send("Đợi em nói xong đã rồi thử lại nha.")
            return
        self.server_data[guild_id]["is_bot_in_use"] = True
        self.voice.play(
            discord.FFmpegPCMAudio("sound/outro.mp3", executable="ffmpeg"))

        while self.voice.is_playing():
            await asyncio.sleep(1)

        self.server_data[guild_id]["is_bot_in_use"] = False

    @commands.command()
    async def stop(self, ctx):
        '''
        Stop playing
        '''
        if self.voice.is_connected():
            await self.voice.disconnect()

    @commands.command()
    async def fb(self, ctx, *, text):
        '''
        Give feedback for author
        '''

        time = datetime.now(self.timezone).strftime('%Y-%m-%d %H:%M:%S')

        with open("feedback.txt", "a") as f:
            f.write(f"[{time}] {ctx.author.name}: {text}\n")
        await ctx.send("Nem sẽ xem feedback khi Nem dệy nha :3")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog '{self.__class__.__name__}' is ready!")

    def get_message(self):
        '''
        Plays message when joins voice channel
        '''

        now = datetime.now()
        day = now.weekday()
        message = [
            "Thứ 2 là ngày đầu buồi", "Đã qua mất một ngày rồi",
            "2 ngày trôi qua nhanh thật nhỉ", "Đã giữa tuần con mẹ nó rồi",
            "Các bạn có biết hôm nay là thứ mấy không? Chính là thứ 6 đó",
            "Wow, ngày nghỉ đầu tiên rồi.",
            "Chưa gì đã hết một ngày, còn mỗi hôm nay để xoã thôi."
        ]

        news = "Em mới được update thêm hàng chờ với thông báo người viết tin nhắn nên là bây giờ mọi người cứ spam thoải mái, không cần lo nha"
        #return message[day] if 0 <= day <= 6 else ""
        return ""


async def setup(bot):
    await bot.add_cog(TTS(bot))

from datetime import datetime

async def ensure_voice_client(guild, channel, server_data):
        guild_id = guild.id
        if guild_id not in server_data or not server_data[guild_id]["connected"]:
            server_data[guild_id] = {
                "voice_client": await channel.connect(),
                "is_bot_in_use": None,
                "default_lang": "vi",
                "message_queue": [],
                "connected": True,
                "vmodel_path": ""
            }
            
        elif server_data[guild_id]["voice_client"].channel != channel:
            await server_data[guild_id]["voice_client"].disconnect()
            server_data[guild_id]["voice_client"] = await channel.connect()

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
        return ''
        return message[day] if 0 <= day <= 6 else ""
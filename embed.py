import discord

def embed_commands(prefix, bot, embed):
    embed.add_field(name = '', value = '-' * 20 + '**Command list**' + '-' * 20, inline=False)
    embed.add_field(name = '', value ='',inline=False)

    for command in bot.commands:
        embed.add_field(name=f"", value=f'**{prefix}{command.name}**: *{command.help}*', inline=False)

    return embed


def embed_llist(llist: dict):
    embed = discord.Embed(title='', color=discord.Color.blue())
    for lang in llist:
        embed.add_field(name= "", value = f"**{lang}**: {llist[lang]}", inline=False)
    return embed

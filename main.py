import os
from discord.ext import commands
import req


url = 'https://www.geeksforgeeks.org/fundamentals-of-algorithms/'
TOKEN = os.environ.get('DISCORD_TOKEN')
GUILD = os.environ.get('DISCORD_GUILD')
r = req.GetContent()
bot = commands.Bot(command_prefix='!')


@bot.command(name='topics', help='Responds list of main topics.')
async def topics(ctx):
    await ctx.send(r.list_string)


@bot.command(name='subtopics', help='Responds with the list of algorithms under the selected subtopic number.')
async def sub(ctx, n: int):
    message = r.get_individual_links(r.lists[n-1])
    msg_part = []
    if len(message) > 1999:
        msg_part = [message[i: i + 2000] for i in range(0, len(message), 2000)]
    else:
        msg_part.append(message)
    for msg in msg_part:
        await ctx.send(msg)


@bot.command(name='get', help='Responds with the selected subtopic from specified topic number')
async def get(ctx, n1: int, n2: int):
    if n1 not in range(1, len(r.links)):
        return
    ol = r.lists[n1 - 1]
    a_tags = ol.find_all('a')
    if n2 not in range(1, len(a_tags)):
        return
    tag = a_tags[n2-1]
    message, code = r.get_final_message(tag.get('href'))
    if code:
        code = '**CODE**\n' + code
    if len(message) > 1999:
        parts = [message[i:i + 2000] for i in range(0, len(message), 2000)]
    else:
        parts = [message]
    if len(code) > 1999:
        code_part = [code[i:i+2000] for i in range(0, len(message), 2000)]
    else:
        code_part = [code]
    for part in parts:
        await ctx.send(part)
    for part in code_part:
        await ctx.send(part)
bot.run(TOKEN)

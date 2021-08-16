import discord
from discord.ext import commands
import os
import numpy as np
import pandas as pd

prefix = '$'

# Make new connection to Discord
#client = discord.Client()
client = commands.Bot(command_prefix = prefix)


cols = {'Frequency':[0]*26}
letters = ['A','B','C','D',
           'E','F','G','H',
           'I','J','K','L',
           'M','N','O','P',
           'Q','R','S','T',
           'U','V','W','X',
           'Y','Z']
df = pd.DataFrame(cols, columns=['Frequency'], index=letters)


""" Create message with five most frequent letters """
def top_five():
    content = "Top Five Letters:\n"
    df.sort_values(by='Frequency', inplace=True, ascending=False)
    top = df.index[0:5]
    for c in top:
        content += "{0}: {1}\n".format(c, df.loc[c]['Frequency'])
    return content


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def top(ctx):
    await ctx.send(top_five())


@client.command()
async def showall(ctx):
    await ctx.send(df)


@client.event
async def on_message(message):
    if message.author != client.user and not message.content.startswith(prefix):
        text = message.content.upper()
        for c in letters:
            df.loc[c] += text.count(c)
    await client.process_commands(message)

    


client.run(os.getenv('TOKEN'))

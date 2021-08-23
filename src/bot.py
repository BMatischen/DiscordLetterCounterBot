import discord
from discord.ext import commands
import os
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

prefix = '$'
# Make new connection to Discord
client = commands.Bot(command_prefix = prefix)


cols = {'Frequency':[0]*26, 'FirstLettFreq':[0]*26}
letters = ['A','B','C','D',
           'E','F','G','H',
           'I','J','K','L',
           'M','N','O','P',
           'Q','R','S','T',
           'U','V','W','X',
           'Y','Z']
df = pd.DataFrame(cols, columns=['Frequency', 'FirstLettFreq'], index=letters)


""" Create message showing five most frequent letters """
def top_five():
    content = "Top Five Most Frequent Letters:\n"
    df.sort_values(by='Frequency', inplace=True, ascending=False)
    top = df.index[0:5]
    ratios = (df['Frequency'] / df['Frequency'].sum()) * 100
    for count, c in enumerate(top):
        content += "{0}. {1}: {2:.2f}%\n".format(count, c, ratios.loc[c])
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


""" Upload bar chart of relative frequencies for first letters of words
    in messages posted to the server """
@client.command(name='plotserverfirstfreq')
async def plot_server_first_freq(ctx):
    # Sort by alphabetical index order
    df.sort_index(inplace=True, ascending=True)
    ratios = (df['FirstLettFreq']/df['FirstLettFreq'].sum())*100

    plt.bar(df.index, ratios, align='edge', width=0.3)
    plt.ylabel("Relative frequency in posted messages (%)")
    plt.title("Relative frequency of first letters of words in server")

    # Write figure to binary stream
    bin_stream = io.BytesIO()
    plt.savefig(bin_stream, format='png')
    plt.close()

    # Create image file to upload using data stream
    bin_stream.seek(0)
    image = discord.File(bin_stream, filename="server_first_letter_frequency.png")
    bin_stream.close()

    await ctx.send(file=image)


""" Upload bar chart of relative frequencies of letters in messages
    posted to the server """
@client.command(name='plotserverfreq')
async def plot_server_freq(ctx):
    # Sort by alphabetical order of index
    df.sort_index(inplace=True, ascending=True)
    ratios = (df['Frequency'] / df['Frequency'].sum()) *100

    plt.bar(df.index, ratios, align='edge', width=0.3)
    plt.ylabel("Relative frequency in posted messages (%)")
    plt.title("Relative frequency of letters in server")

    # Save figure to binary stream
    bin_stream = io.BytesIO()
    plt.savefig(bin_stream, format='png')
    plt.close()

    # Create image file to upload using data stream
    bin_stream.seek(0)
    image = discord.File(bin_stream, filename="server_letter_frequency.png")
    bin_stream.close()

    await ctx.send(file=image)


""" Count letters and first letters of words in new messages """
@client.event
async def on_message(message):
    # Don't count commands for bot or its messages
    if message.author != client.user and not message.content.startswith(prefix):
        text = message.content.upper().split()
        for word in text:
            for c in letters:
                df.loc[c]['Frequency'] += word.count(c)
                if c == word[0]:
                    df.loc[c]['FirstLettFreq'] += 1

    # Allow bot to process commands when this function is called
    await client.process_commands(message)

    


client.run(os.getenv('TOKEN'))

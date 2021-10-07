# Import modules
import collections
import random
import re
import discord
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Load .env file and token
env_path = Path('/home/plank/scripts/')/'.env'
load_dotenv(dotenv_path=env_path)
client = discord.Client()
TOKEN = os.getenv("DISCORD_TOKEN")


# Log in to Discord
@client.event
async def on_ready():
    print('We have logged in as {0.user}. Hitch your tits and pucker up, it\'s time to peel the paint!'.format(client))


# Wait for a message
@client.event
async def on_message(message):
    userfull = str(message.author)
    user, idnum = userfull.split("#")
    icon = message.author.avatar_url
    results = []

# If the bot sent the message, ignore it
    if message.author.id == client.user.id:
        return

# Print how many servers the bot is connected to
    if message.content.startswith('!servers'):
        if len(client.guilds) == 1:
            await message.channel.send("I'm in " + str(len(client.guilds)) + " server!")
        else:
            await message.channel.send("I'm in " + str(len(client.guilds)) + " servers!")

# Bobbie!
    if message.content.startswith('!bobbie'):
        await message.channel.send(file=discord.File('/home/plank/images/bobbie.gif'))
        await message.delete()

# Wait for message starting with "!e"

    if message.content.startswith('!e'):

        # Declare some variables
        msg = message.content
        word_count = len(msg.split())
        msg_list = msg.split()
        dice = str("1d6")
        bonus = 0
        desc = str("")
        special_char = re.compile('[@_!#$%^&*()<>?/|}{~:]')

        # Figure out what the user sent and update variables accordingly
        if word_count == 4:
            arg, dice, bonus, desc = msg.split(" ")

        if word_count == 3 and special_char.search(msg_list[-1]):
            arg, dice, desc = msg.split(" ")
            bonus = 0
        if msg_list[-1].isalpha() and word_count == 3 and (special_char.search(msg_list[-1]) is None):
            arg, dice, desc = msg.split(" ")
            bonus = 0
        if msg_list[-1].isnumeric() and word_count == 3:
            arg, dice, bonus = msg.split(" ")
            desc = str("")
        if word_count == 2:
            arg, dice = msg.split(" ")
            bonus = 0
            desc = str("")

        # Use regex to validate xdy format
        if not re.search("^[0-9].*[d]*[0-9].*", dice):
            return

        # Stringify and concatenate some variables for output
        desc = str(desc)
        bonus = str(bonus)
        dice = str(dice)
        q, sides = dice.split("d")
        msg = str("**" + dice + "** + " + "***" + bonus + "***" + "\n\n")
        count = int(q)
        sides = int(sides)
        total = int(bonus)

        # Roll the dice!
        while int(count) > 0:
            a = random.randint(1, sides)
            a = int(a)
            results.append(a)
            count -= 1
        count = collections.Counter(results)

        # Identify matches and adjust output
        for a in count:
            if count[a] > 1:
                for g in range(count[a]):
                    r = str(a)
                    a = str(a)
                    msg += ("**" + r + "** + ")
            else:
                a = str(a)
                msg += a + " + "

        # Iterate through the rolls to build total
        for ele in range(0, len(results)):
            total = total + results[ele]
        bonus = str(bonus)
        total = str(total)

        # Format final output
        msg += "*" + bonus + "*" + " = " + "**" + total + "**"
        if dice == "3d6":
            drama = str(results[-1])
            msg += ("\n\n" + " ឵឵឵ ឵឵ ឵឵ ឵឵ ឵឵ ឵឵឵DRAMA\n" + "```css\n   [" + drama + "]```")
        if desc != str(""):
            msg = "```ini\n[" + desc + "]```\n" + msg

        # Define embeds
        embed = discord.Embed(description=msg, color=discord.Color.random(), inline=True)
        embed.set_author(name=user, icon_url=icon)

        # Delete triggering user message
        await message.delete()

        # Send the completed message
        await message.channel.send(embed=embed)

    # Clear the results list for next roll
    del results
client.run(TOKEN)

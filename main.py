# Import libraries
import collections
import random
import re
import discord
import os
from dotenv import load_dotenv


file = open("/home/plank/txt/churn.txt", "r")
churn = file.read()
file.close()

# Load .env file and token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = discord.Client(intents=discord.Intents.all())

# Verify login to Discord
@client.event
async def on_ready():
    print('We have logged in as {0.user}. Hitch your tits and pucker up, it\'s time to peel the paint!'.format(client))

# Wait for a message
@client.event
async def on_message(message):
    global churn
    userfull = str(message.author)
    user, idnum = userfull.split("#")
    icon = message.author.avatar.url
    results = []
    with open("/home/plank/txt/churn.txt", "r") as file2:
        churn = file2.read()

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

# Amos!
    if message.content.startswith('!amos'):
        await message.channel.send(file=discord.File('/home/plank/images/amos.gif'))
        await message.delete()

    # Churn Tracker
    if message.content.startswith('!churn'):
        churn_input = message.content
        churn_word_count = len(churn_input.split())
        if churn_word_count == 2:
            arg, churn_change = churn_input.split()

            # Set churn to zero if 'reset' is sent instead of a number
            if churn_change == "reset":
                churn = str("0")
                with open("/home/plank/txt/churn.txt", "w") as file2:
                    file2.write(churn)
                    file2.close()
                await message.channel.send("Churn has been reset to zero.")
                await message.channel.send(file=discord.File('/home/plank/images/churn_' + churn + ".png"))
                await message.delete()

            # Update churn if numerical input sent
            if churn_change.lstrip("-+").isnumeric():
                churn = int(churn)
                churn_change = int(churn_change)
                churn = churn_change + churn
                if churn > 30:
                    churn = churn - 30
                if churn < 0:
                    churn = 0
                with open("/home/plank/txt/churn.txt", "w") as file2:
                    churn = str(churn)
                    file2.write(churn)
                    file2.close()
                    await message.channel.send(file=discord.File('/home/plank/images/churn_' + churn + ".png"))
                    await message.delete()
                with open("churn.txt", "r") as file2:
                    churn = file2.read()
                    file2.close()
                    await message.channel.send(file=discord.File('/home/plank/images/churn_' + churn + ".png"))
                    await message.delete()

        # Display current churn
        if churn_word_count == 1:
            await message.channel.send(file=discord.File('/home/plank/images/churn_' + churn + ".png"))
            await message.delete()

        if churn_word_count == 2:
            churn_arg, churn_change = churn_input.split()
            if churn_change.isnumeric():
                churn += churn_change
                with open("/home/plank/txt/churn.txt", "w") as f:
                    f.seek(0)
                    f.write(churn)
                    f.truncate()
                    f.close()

    # Wait for message starting with "!e"

    if message.content.startswith('!e'):

        # Declare some variables
        msg = message.content
        word_count = len(msg.split())
        msg_list = msg.split()
        dice = str("1d6")
        bonus = 0
        desc = str("")
        special_char = re.compile("[@_!#$%^&*()<>?/\\\\|}{~:]")

        # Figure out what the user sent and update variables accordingly
        if word_count == 4:
            arg, dice, bonus, desc = msg.split(" ")

        if word_count == 3 and special_char.search(msg_list[-1]):
            arg, dice, desc = msg.split(" ")
            bonus = 0
        if msg_list[-1].isalpha() and word_count == 3 and (special_char.search(msg_list[-1]) is None):
            arg, dice, desc = msg.split(" ")
            bonus = 0
        if msg_list[-1].lstrip("-+").isnumeric() and word_count == 3:
            arg, dice, bonus = msg.split(" ")
            desc = str("")
        if word_count == 2:
            arg, dice = msg.split(" ")
            bonus = 0
            desc = str("")
        if word_count == 1:
            dice = "3d6"
            bonus = 0
            desc = str("")

        # Use regex to validate xdy format
        if not re.search("^[0-9].*[d]*[0-9].*", dice):
            return

        # Stringify, integerize, and concatenate some variables for output
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
                for _ in range(count[a]):
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
        embed = discord.Embed(description=msg, color=discord.Color.random())
        embed.set_author(name=user, icon_url=icon)

        # Delete triggering user message
        await message.delete()

        # DM the message to the sending user and send a message to the channel
        if message.content.startswith('!edm'):
            dm_msg_list = (
                user + " is sealing your fate. <a:meow_popcorn:897966437556183050>",
                user + " is deciding whether to space you or not. <a:meow_popcorn:897966437556183050>",
                "Get ready for the juice, " + user + " is rolling in secret. <a:meow_popcorn:897966437556183050>",
                "Don't worry, I'm sure " + user + " is just rolling dice for fun. <a:meow_popcorn:897966437556183050>"
            )

            await message.author.send(embed=embed)
            await message.channel.send(random.choice(dm_msg_list))
            return

        # Send the message to the channel
        else:
            await message.channel.send(embed=embed)

    # Clear the results list for next roll
    del results

# Run the bot
client.run(TOKEN)

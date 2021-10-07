import collections
import random
import re
import discord

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}. Hitch your tits and pucker up, it\'s time to peel the paint!'.format(client))


@client.event
async def on_message(message):
    userfull = str(message.author)
    user, idnum = userfull.split("#")
    icon = message.author.avatar_url
    results = []

    if message.author.id == client.user.id:
        return

    if message.content.startswith('!servers'):
        if len(client.guilds) == 1:
            await message.channel.send("I'm in " + str(len(client.guilds)) + " server!")
        else:
            await message.channel.send("I'm in " + str(len(client.guilds)) + " servers!")

    if message.content.startswith('!bobbie'):
        await message.channel.send(file=discord.File('/home/plank/images/bobbie.gif'))
        await message.delete()

    if message.content.startswith('!e'):
        msg = message.content
        word_count = len(msg.split())
        msg_list = msg.split()
        dice = str("1d6")
        bonus = 0
        desc = str("")
        special_char = re.compile('[@_!#$%^&*()<>?/|}{~:]')

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

        if not re.search("^[0-9].*[d]*[0-9].*", dice):
            return

        desc = str(desc)
        bonus = str(bonus)
        dice = str(dice)
        q, sides = dice.split("d")
        msg = str("**" + dice + "** + " + "***" + bonus + "***" + "\n\n")
        count = int(q)
        sides = int(sides)
        total = int(bonus)

        while int(count) > 0:
            a = random.randint(1, sides)
            a = int(a)
            results.append(a)
            count -= 1
        count = collections.Counter(results)
        for a in count:
            if count[a] > 1:
                for g in range(count[a]):
                    r = str(a)
                    a = str(a)
                    msg += ("**" + r + "** + ")
            else:
                a = str(a)
                msg += a + " + "
        for ele in range(0, len(results)):
            total = total + results[ele]
        bonus = str(bonus)
        total = str(total)
        msg += "*" + bonus + "*" + " = " + "**" + total + "**"
        if dice == "3d6":
            drama = str(results[-1])
            msg += ("\n\n" + " ឵឵឵ ឵឵ ឵឵ ឵឵ ឵឵ ឵឵឵DRAMA\n" + "```css\n   [" + drama + "]```")
        if desc != str(""):
            msg = "```ini\n[" + desc + "]```\n" + msg
        embed = discord.Embed(description=msg, color=discord.Color.random(), inline=True)
        embed.set_author(name=user, icon_url=icon)
        await message.delete()
        await message.channel.send(embed=embed)
    del results
client.run('ODkyNDM0MTQ3NzgyNTY1ODkw.YVM2EQ.edtdJLe0sZc3IDNgwRIiiPHRt7g')
# client.run(os.getenv('TOKEN'))

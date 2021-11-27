import discord
import os
from random import randrange

client = discord.Client()

playing = False
randomNumber = randrange(10)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    global playing
    global randomNumber
    if message.author == client.user:
        return
    if playing:
        try:
            content = message.content
            if content == "quit":
                playing = False
                await message.channel.send("Quitting the game, the answer was: " + str(randomNumber))
                return
            answer = int(content)
            if answer == randomNumber:
                await message.channel.send("Congratulations")
                playing = False
            else:
                await message.channel.send("Try again")
        except ValueError:
            await message.channel.send("That is not a number")
    else:
        if message.content.startswith('$play'):
            await message.channel.send("Guess the number [0-9] (type quit to quit)")
            randomNumber = randrange(10)
            playing = True

client.run(os.getenv("TOKEN"))

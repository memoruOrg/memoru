import discord
from data_base import data_base
from dropdown import DropDown
import answer_button
from discord.ui import View

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[914264804171079702], description="Create a new card")
async def new(ctx: discord.ApplicationContext, front: str, back: str):
    if data_base.add(ctx.author.id, front, back):
        await ctx.respond("Card created")
    else:
        await ctx.respond("A card with that front already exists")

@bot.slash_command(guild_ids=[914264804171079702], description="Start a Memorum session")
async def ask(ctx):
    await answer_button.ask(ctx)

@bot.slash_command(guild_ids=[914264804171079702], description="Select cards to delete them")
async def delete(ctx):
    if data_base.isEmpty(ctx.author.id):
        return await ctx.respond("No cards yet")
    view = View(DropDown(ctx.author.id))
    await ctx.respond("Question log:", view=view)

@bot.slash_command(guild_ids=[914264804171079702], description="Set all Cards fields to their default. Preserve \"front\" and \"back\" fields")
async def reset(ctx):
    data_base.reset(ctx.author.id)

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
bot.run(token)

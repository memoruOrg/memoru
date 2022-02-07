import discord
from DataBase import data_base
from discord.ui import Button, View, Select

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[914264804171079702])
async def new(ctx: discord.ApplicationContext, question: str, answer: str): # Conseguir tipo de verdad ctx
    print(ctx.author.id)
    data_base.add(ctx.author.id, question, answer)
    await ctx.respond("Card created")

# Start session
class AnswerButton(Button):
    quality: int
    cardIndex: int
    # ctx: discord.Context
    def __init__(self, label: int, card, ctx):
        self.quality = label
        self.ctx = ctx
        self.card = card
        super().__init__(label=str(label))

    async def callback(self, interaction: discord.Interaction):
        data_base.update_quality(self.ctx.author.id, self.card, self.quality)
        continueButton = Button(label="Continue", style=discord.ButtonStyle.green)
        closeButton =  Button(label="End Session", style=discord.ButtonStyle.red)
        async def continueButtonCallback(interaction: discord.Interaction):
            await interaction.response.edit_message(view=None)
            await ask(self.ctx)
        async def closeButtonCallback(interaction: discord.Interaction):
            await interaction.response.edit_message(view=None)
        continueButton.callback = continueButtonCallback
        closeButton.callback = closeButtonCallback
        await interaction.response.edit_message(view=View(continueButton, closeButton))

@bot.slash_command(guild_ids=[914264804171079702])
async def ask(ctx):
    if data_base.isEmpty(ctx.author.id):
        return await ctx.respond("No cards yet")
    card = data_base.get(ctx.author.id)
    print("bool: ", data_base.db[str(ctx.author.id)].find_one())
    viewButtons = View()
    for i in range(6):
        viewButtons.add_item(AnswerButton(i, card, ctx))
    buttonAnswer = Button(label="See reverse", emoji="🙏")
    viewAnswer = View(buttonAnswer)
    async def buttonAnswerCallback(interaction: discord.Interaction):
        await interaction.response.edit_message(view=None)
        await interaction.followup.send("Reverse: " + card["answer"], view=viewButtons)
    buttonAnswer.callback =  buttonAnswerCallback
    await ctx.respond("Cara: " + card["question"], view=viewAnswer)

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

class Dropdown(Select):
    def __init__(self, id_user):
        options = []
        self.id_user = id_user
        for card in data_base.get_all(id_user):
            options.append(discord.SelectOption(label=card['question'], description=card['answer']))
        super().__init__(
            max_values=len(options) if len(options) <= 25 else 25,
            min_values=1,
            options=options,
            placeholder="Choose the cards to be deleted"
                     )
    async def callback(self, interaction: discord.Interaction):
        out = "Question" if len(self.values) == 1 else "Questions"
        await interaction.response.edit_message(content=out + " successfully eliminated", view=None)
        data_base.delete(self.id_user, self.values)

@bot.slash_command(guild_ids=[914264804171079702])
async def delete(ctx):
    if data_base.isEmpty(ctx.author.id):
        return await ctx.respond("No cards yet")
    view = View(Dropdown(ctx.author.id))
    await ctx.respond("Question log:", view=view)

token = read_token()
bot.run(token)

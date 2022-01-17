import discord
from Card import cardSlice
from discord.ui import Button, View

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[914264804171079702])
async def new(ctx: discord.ApplicationContext, question: str, answer: str): # Conseguir tipo de verdad ctx
    # print(ctx.author.id)
    cardSlice.add(question, answer)
    await ctx.respond("Tarjeta creada")

# Start session
class AnswerButton(Button):
    quality: int
    cardIndex: int
    def __init__(self, label: int, ctx):
        self.quality = label
        self.ctx = ctx
        super().__init__(label=str(label))

    async def callback(self, interaction: discord.Interaction):
        cardSlice.updateQuality(self.quality)
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
    card = cardSlice.get()
    viewButtons = View()
    for i in range(6):
        viewButtons.add_item(AnswerButton(i, ctx))
    buttonAnswer = Button(label="Show Answer")
    viewAnswer = View(buttonAnswer)
    async def buttonAnswerCallback(interaction: discord.Interaction):
        await interaction.response.edit_message(view=None)
        await interaction.followup.send("Answer: " + card.answer , view=viewButtons)
    buttonAnswer.callback =  buttonAnswerCallback
    await ctx.respond("Question: " + card.question, view=viewAnswer)

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
bot.run(token)

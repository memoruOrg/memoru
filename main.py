import discord
import Card
from discord.ui import Button, View

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[914264804171079702])
async def new(ctx: discord.ApplicationContext, question: str, answer: str):
    # print(ctx.author.id)
    Card.cardSlice.add(question, answer)
    await ctx.respond("Carta creada")

# Start session
class AnswerButton(Button):
    quality: int
    card: list = []
    def __init__(self, label: int, card):
        self.quality = label
        self.card = card
        super().__init__(label=str(label))

    async def callback(self, interaction: discord.Interaction):
        # Aplicar value a question
        # print(self.value)
        continueButton = Button(label="Continue", style=discord.ButtonStyle.green)
        closeButton =  Button(label="End Session", style=discord.ButtonStyle.red)
        async def closeButtonCallback(interaction: discord.Interaction):
            await interaction.response.edit_message(view=None)
        closeButton.callback = closeButtonCallback
        await interaction.response.edit_message(view=View(continueButton, closeButton))

@bot.slash_command(guild_ids=[914264804171079702])
async def ask(ctx):
    viewButtons = View()
    for i in range(6):
        viewButtons.add_item(AnswerButton(i, Card.cardSlice[0]))
    buttonAnswer = Button(label="Show Answer")
    viewAnswer = View(buttonAnswer)
    async def buttonAnswerCallback(interaction: discord.Interaction):
        await interaction.response.send_message(Card.cardSlice[0][1], view=viewButtons)
    buttonAnswer.callback =  buttonAnswerCallback
    await ctx.respond(Card.cardSlice[0][0], view=viewAnswer)

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
bot.run(token)

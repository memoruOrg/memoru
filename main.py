import discord
from discord.ui import Button, View

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[914264804171079702])
async def new(ctx):
    await ctx.respond("Hello!")

# Start session
class AnswerButton(Button):
    value: str = ""
    question: str
    def __init__(self, label: str):
        self.value = label
        super().__init__(label=label)

    async def callback(self, interaction: discord.Interaction):
        # Aplicar value a question
        continueButton = Button(label="Continue", style=discord.ButtonStyle.green)
        closeButton =  Button(label="End Session", style=discord.ButtonStyle.red)
        async def closeButtonCallback(interaction: discord.Interaction):
            await interaction.response.edit_message(view=None)
        closeButton.callback = closeButtonCallback
        await interaction.response.edit_message(view=View(continueButton, closeButton))

@bot.slash_command(guild_ids=[914264804171079702])
async def ask(ctx):
    view = View()
    for i in range(6):
        view.add_item(AnswerButton(str(i)))
    await ctx.respond("¿Cuanto es 2+2?", view=view)


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()

token = read_token()
bot.run(token)

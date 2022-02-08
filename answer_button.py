import discord
from discord.ui import Button, View
from data_base import data_base
from time import time

time_answer: float

class answer_button_(Button):
    quality: int
    cardIndex: int
    # ctx: discord.Context
    def __init__(self, label: int, card, ctx):
        self.quality = label
        self.ctx = ctx
        self.card = card
        super().__init__(label=str(label))

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            return await interaction.response.send_message(content="You are not allowed to do this", ephemeral=True)
        global time_answer
        data_base.update_quality(self.ctx.author.id, self.card, self.quality, time_answer)
        time_answer = 0
        continueButton = Button(label="Continue", style=discord.ButtonStyle.green)
        closeButton =  Button(label="End Session", style=discord.ButtonStyle.red)
        async def continueButtonCallback(interaction: discord.Interaction):
            if interaction.user.id != self.ctx.author.id:
                return await interaction.response.send_message(content="You are not allowed to do this", ephemeral=True)
            await interaction.response.edit_message(view=None)
            await ask(self.ctx)
        async def closeButtonCallback(interaction: discord.Interaction):
            if interaction.user.id != self.ctx.author.id:
                return await interaction.response.send_message(content="You are not allowed to do this", ephemeral=True)
            await interaction.response.edit_message(view=None)
        continueButton.callback = continueButtonCallback
        closeButton.callback = closeButtonCallback
        await interaction.response.edit_message(view=View(continueButton, closeButton))

async def ask(ctx):
    if data_base.isEmpty(ctx.author.id):
        return await ctx.respond("No cards yet")
    card = data_base.get(ctx.author.id)
    viewButtons = View()
    for i in range(6):
        viewButtons.add_item(answer_button_(i, card, ctx))
    start_time: float
    buttonAnswer = Button(label="See reverse", emoji="🙏")
    async def buttonAnswerCallback(interaction: discord.Interaction):
        if interaction.user.id != ctx.author.id:
            return await interaction.response.send_message(content="You are not allowed to do this", ephemeral=True)
        global time_answer
        time_answer = time() - start_time
        await interaction.response.edit_message(view=None)
        await interaction.followup.send("Reverse: " + card["answer"], view=viewButtons)
    buttonAnswer.callback =  buttonAnswerCallback
    viewAnswer = View(buttonAnswer)
    await ctx.respond("Front: " + card["question"], view=viewAnswer)
    start_time = time()

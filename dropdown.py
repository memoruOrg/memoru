import discord
from discord.ui import Select
from data_base import data_base

class DropDown(Select):
    def __init__(self, id_user):
        options = []
        self.id_user = id_user
        for card in data_base.get_all(id_user):
            options.append(discord.SelectOption(label=card['question'], description=card['answer']))
        super().__init__(
            max_values=len(options) if len(options) <= 25 else 25,
            # min_values=1,
            options=options,
            placeholder="Choose the cards to be deleted"
                     )
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.id_user:
            return await interaction.response.send_message(content="You are not allowed to do this", ephemeral=True)
        out = "Question" if len(self.values) == 1 else "Questions"
        await interaction.response.edit_message(content=out + " successfully eliminated", view=None)
        data_base.delete(self.id_user, self.values)

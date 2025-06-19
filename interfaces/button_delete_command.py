#Discord
import discord
from discord import ButtonStyle
from discord.ui import Button

# Fonctions statiques
from json_processor.command_json import CommandJson

class ButtonDeleteCommand(Button):
    def __init__(self, username: str, user_id: int):
        super().__init__(style=ButtonStyle.red, label="Supprimez la commande")
        self.username = username
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction) -> bool:
        success = True

        try :
            CommandJson.set_command_json_variable(None, None, interaction.channel.name, "instant_messaging", 0) # Arrêt du système de conversation instannée
            CommandJson.set_command_json_variable(self.username, self.user_id, None, "command_etat", 1)         # Mise en etat command à supprimer
        except :
            success = False

        return success


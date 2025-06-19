#Discord
import discord
from discord import ButtonStyle
from discord.ui import Button

# Fonctions statiques
from json_processor.command_json import CommandJson
import bots.utils.discord_management as DM

class ButtonCreateCommand(Button):
    def __init__(self)  -> None:
        # Définis le style et le label du bouton
        super().__init__(style=ButtonStyle.green, label="Prendre la commande")

    async def callback(self, interaction: discord.Interaction)  -> bool:
        success = True

        try :
            CommandJson.set_command_json_variable(None, None, interaction.channel.name, "instant_messaging", 1)             # Démarrage du système de conversation instannée
            CommandJson.set_command_json_variable(None, None, interaction.channel.name, "cooker_id", interaction.user.id)   # Assigne  le cuisinier à la commande

            await DM.DiscordManagement.set_private_channel_to_member(interaction)
            await DM.DiscordManagement.send_message_to_channel_by_interaction(interaction, "Ce ticket est maintenant le vôtre")
        except :
            success = False

        return success
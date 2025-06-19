#Discord
import discord
from discord import ButtonStyle
from discord.ui import Button

# Fonctions statiques
from json_processor.command_json import CommandJson
from json_processor.blacklist_json import BlacklistJson
import bots.utils.discord_management as DM

class ButtonAddToBlacklist(Button):

    def __init__(self, username: str, user_id: int) -> None:

        super().__init__(style=ButtonStyle.primary, label="Mettre en liste noir")
        self.username = username
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction) -> bool:
        success = True

        try :
            CommandJson.set_command_json_variable(self.username, self.user_id, None, "command_etat", 1) # Mise en etat command à supprimer
            BlacklistJson.add_to_blacklist(self.user_id)                                                # Ajout de l'utilisateur dans la blacklist permettant de l'empêcher de faire de nouvelle commande
            await DM.DiscordManagement.send_message_to_channel_by_interaction(interaction, "Cette utilisateur est maintenant interdit de passer des commandes : ")
        except:
            success = False

        return success


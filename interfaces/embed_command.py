import discord
import operator

# CLass interface
from interfaces.buttons_style import ButtonsStyle
from utils.file_management import FileManagement
from json_processor.loyalty_json import LoyaltyJson
from json_processor.stats_json import StatsJson

class EmbedCommand():

    def __init__(self, ctx, channel)  -> None:
        self.ctx = ctx
        self.channel = channel

    async def send_embed_command(self, data, username, user_id) -> bool:
        success = True

        try :
            view = ButtonsStyle(username, user_id)

            embed = discord.Embed(title="Ticket information", color=0x7289DA)
            embed.add_field(name="Username", value=username, inline=False)
            embed.add_field(name="Address", value=data.get("address"), inline=False)
            embed.add_field(name="Prix", value=data.get("price"), inline=False)

            photo_path = FileManagement.get_command_jpg_path(username)
            photo_file_name = FileManagement.get_command_jpg_file_name(username)

            embed.set_image(url="attachment://" + photo_file_name)
            file = discord.File(photo_path, filename=photo_file_name)

            await self.channel.send(embed=embed, file=file, view=view)

        except :
            success = False

        return success

    async def send_embed_leaderboard(self) -> bool:
        success = True

        try :
            data_fidelite = LoyaltyJson.get_json_file()
            users_sorted_points = sorted(data_fidelite, key=operator.itemgetter("points"), reverse=True) # Trie les points du plus grand au plus petit.

            embed = discord.Embed(title="TOP10 des points de fidélité", color=discord.Color.blue())

            for idx, user in enumerate(users_sorted_points[:10], start=1): # idx permet de récupérer l'indice auquel nous somme dans la liste.
                user_id = user["username"]
                points = user["points"]
                username = user_id

                embed.add_field(name=f"{idx}. {username}", value=f"{points} points", inline=False)

            await self.ctx.send(embed=embed)

        except :
            success = False

        return success

    async def send_embed_stats(self) -> bool:
        success = True

        try :
            embed = discord.Embed(title="Statistique des ventes", color=discord.Color.blue())
            data_stats = StatsJson.get_json_file()

            for key, value in data_stats.items():
                embed.add_field(name=key, value=value, inline=False)

            await self.ctx.send(embed=embed)

        except :
            success = False

        return success

    async def send_embed_help(self, bot_discord) -> bool:
        success = False

        try :

            embed = discord.Embed(title="Liste des commandes", color=discord.Color.blue())

            commands_list = bot_discord.commands

            for command in commands_list:
                if command.name != 'help':
                    embed.add_field(name=f"!{command.name}", value=command.help, inline=False)

            await self.ctx.send(embed=embed)

        except :
            success = True

        return success

    async def send_embed_points(self, username, points) -> bool:
        success = False

        try :
            embed = discord.Embed(title="Points de fidélité", color=discord.Color.blue())
            if points is not None:
                embed.add_field(name="", value=f"{username} : {points} points", inline=False)
            else :
                embed.add_field(name="", value=f"{username} n'a pas de point de fidélité.", inline=False)

            await self.ctx.send(embed=embed)
        except :
            success = True

        return success

    async def send_embed_channels_canceled(self, counter) -> bool:
        success = True

        try :
            if counter <= 1:
                text = "channel supprimé."
            else :
                text = "channels supprimés."

            embed = discord.Embed(title="Suppression commandes annulées", color=discord.Color.blue())
            embed.add_field(name="", value=f"{counter} {text}", inline=False)
            await self.ctx.send(embed=embed)
        except :
            success = False

        return success
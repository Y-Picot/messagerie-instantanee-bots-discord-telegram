
import discord
from typing import Optional

from utils.constants import SERVEUR_DISCORD_ID
import interfaces.embed_command as EC
from json_processor.command_json import CommandJson

class DiscordManagement():

    # Server
    def get_discord_server(bot_discord) -> Optional[discord.Guild]:
        return bot_discord.get_guild(SERVEUR_DISCORD_ID)

    def get_channel_discord_server(bot_discord, command_user) -> Optional[discord.TextChannel]:
        channel = None

        server =  DiscordManagement.get_discord_server(bot_discord)
        if server is None:
            print("Le serveur discord n'existe pas : get_channel_discord_server()")
        else :
            channel = discord.utils.get(server.text_channels, name=command_user)
            if channel is None:
                print("Le channel n'existe pas : get_channel_discord_server()")
        return channel

    # Channels
    async def delete_channels(ctx, bot_discord, channel_name_to_delete) -> bool:
        counter = 0
        sucess = False
        server = DiscordManagement.get_discord_server(bot_discord)

        for channel in server.text_channels :
            if channel.name == channel_name_to_delete:
                await channel.delete()
                counter += 1
                sucess = True
                print("Channel deleted.")

        embed_command = EC.EmbedCommand(ctx, None)
        await embed_command.send_embed_channels_canceled(counter)

        return sucess

    async def create_channel_user_command(bot_discord, data, username, user_id, channel_name) -> bool:
        sucess = True

        server =  DiscordManagement.get_discord_server(bot_discord)
        if server is None:
            sucess = False

        channel = discord.utils.get(server.text_channels, name=channel_name)
        # Création du channel discord
        if channel is None: # Si le channel discord n'existe pas
            channel = await server.create_text_channel(channel_name)
            embed_command = EC.EmbedCommand(None, channel)
            await embed_command.send_embed_command(data, username, user_id)

        CommandJson.set_command_json_variable(username, user_id, None, "ticket_etat", 1)

        return sucess

    async def set_channel_name_command_canceled(bot_discord, channel_name, interaction) -> bool:
        sucess = True
        existing_channel = None

        if interaction is not None :
            existing_channel = interaction.channel
        elif bot_discord is not None and channel_name is not None :
            existing_channel = DiscordManagement.get_channel_discord_server(bot_discord, channel_name)
        else :
            print("Le channel discord est introuvable : set_channel_name_command_canceled()")
            sucess = False

        if existing_channel is not None :
            await existing_channel.edit(name="Commande-annulee")
            await existing_channel.send("Commande annulée")

        return sucess

    async def set_private_channel_to_member(interaction) -> bool:
        sucess = False
        try :
            await interaction.channel.set_permissions(interaction.user, read_messages=True)                         # Le membre peut voir le channel
            await interaction.channel.set_permissions(interaction.guild.default_role, read_messages=False)          # @everyone ne voit plus le channel
            sucess = True
        except Exception as e :
            print("Quelques choses ne va pas : set_private_channel_to_member() "+ str(e))
        return sucess

    async def set_channel_to_view_only_for_member(channel, member) -> bool:
        # Non utiliser pour l'instant
        sucess = False
        try :
            await channel.set_permissions(member, send_messages=False, read_messages=True)
            sucess = True
        except Exception as e :
            print("Quelques choses ne va pas : set_private_channel_to_member() "+ str(e))
        return sucess

    async def set_channel_private_and_purged(bot_discord, channel_name) -> bool:
        success = False
        channel = DiscordManagement.get_channel_discord_server(bot_discord, channel_name)
        guild = DiscordManagement.get_discord_server(bot_discord)
        if channel :

            for target, overwrite in channel.overwrites.items():                    # Supprime toutes les autorisations existantes sur le canal
                await channel.set_permissions(target, overwrite=None)

            await channel.set_permissions(guild.default_role, view_channel=False)   # Mets le channels en privée pour le groupe everyone
            success = True
        else :
            print("Le channel n'existe pas : set_channel_private_and_purged()")
        return success

    # Gestion paramètre des commandes
    async def get_everything_but_discord_commands(ctx, message_error) -> Optional[str]:
        content = None
        try :
            content_split = ctx.message.content.split(' ', 1)

        except Exception as e :
            print("Le message n'as pas pu être découper : get_var1_message() "+ str(e))

        if len(content_split) > 1: # Si il y a un message
            content = content_split[1]
        else:
            await ctx.send(message_error)
        return content

    # Messages
    async def send_message_to_channel_by_interaction(interaction, message) -> bool:
        sucess = False
        if interaction is not None:
            await interaction.response.send_message(message +" "+ interaction.user.name, ephemeral=True)
            sucess = True
        return sucess


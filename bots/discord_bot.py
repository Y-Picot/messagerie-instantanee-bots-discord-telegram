import os
from queue import Empty
import asyncio

#Discord
from discord.ext import commands, tasks
import discord

# Constantes
from utils.constants import DISCORD_BOT_TOKEN_SECONDARY, DISCORD_SERVER_ID, AUTHORIZED_DISCORD_USERS, JSON_COMMANDS_PATH

# Fonctions
from json_processor.command_json import CommandJson
from json_processor.announcement_json import AnnouncementJson
from json_processor.loyalty_json import LoyaltyJson
from json_processor.stats_json import StatsJson

# from bots.utils.discord_management import DiscordManagement
from utils.file_management import FileManagement
import interfaces.embed_command as EC
import bots.utils.discord_management as DM # Les imports étant utiliser à plusieurs endroit, un import à la carte est utilisé.

# Initialisation du bot Discord
def init_bot_discord() -> commands.Bot:
    intents = discord.Intents.all()
    intents.typing = False
    intents.presences = False
    bot = commands.Bot(command_prefix='!', intents=intents)
    bot.remove_command('help')
    return bot

# Initialisation
bot_discord = init_bot_discord()
DISCORD_TOKEN = DISCORD_BOT_TOKEN_SECONDARY

## Asyncio Taks

# Lecture de tous les tickets définis dans les fichiers json
async def check_for_tickets() -> None:

    while True:
        for filename in os.listdir(JSON_COMMANDS_PATH):                                                                  # Récupération de tous les fichiers

            if FileManagement.format_well_formed(filename):

                data = CommandJson.get_command_json_by_filename(JSON_COMMANDS_PATH + filename)
                if data is not None:

                    username = data.get("username")
                    user_id = data.get("user_id")
                    command_name = FileManagement.get_command_channel_name(username, user_id)

                    if data.get("ticket_etat") != 1:                                                                    # Si le channel discord n'a pas encore été créer
                        await DM.DiscordManagement.create_channel_user_command(bot_discord, data, username, user_id, command_name)

                    if data.get("command_etat") == 1:                                                                   # Si la commande est annulée
                        FileManagement.remove_command_files(username, user_id)                                          # Suppression du fichier .json et de la photo .jpg
                        await DM.DiscordManagement.set_channel_private_and_purged(bot_discord, command_name)            # Reset les droits et met le channel en privée
                        await DM.DiscordManagement.set_channel_name_command_canceled(bot_discord, command_name, None)   # Modifie le nom du channel

                else :
                    #"Data renvoie None : check_for_tickets()")
                    pass
            else :
                #"Fichier malformé : check_for_tickets()")
                pass
        await asyncio.sleep(1)

# Regarde si un message de telegram est arrivé
async def check_messages() -> None:
    guild = bot_discord.get_guild(DISCORD_SERVER_ID)
    while True:
        try:
            origine, message = queue_bots.get_queue_telegram().get(timeout=0.5) # Récupérer le dernier message de la queue

            if CommandJson.search_command_json_variable(None, None, origine, "instant_messaging"): # Si la conversation instantanée est lancée pour ce ticket

                concerned_channel = discord.utils.get(guild.text_channels, name=origine)
                await concerned_channel.send(message)

        except Empty:
            pass
        await asyncio.sleep(1)

# Permet de mettre les deux coroutine en route en asynchrone sur le thread de Discord
async def asyncio_taks() -> None:
    await asyncio.gather(
        check_for_tickets(),
        check_messages(),
    )

#### Commandes
@bot_discord.command(name='test')
async def test_command(ctx) -> None:
    """
    Tester si le bot est en ligne.
    """
    await ctx.send('Test réussi ! Discord')

@bot_discord.command(name='supprime_commandes_annulees')
async def delete_all_command_canceled(ctx) -> None:
    """
    Supprimer tous les channels nommés commande-annulee.
    """

    if ctx.author.id in AUTHORIZED_DISCORD_USERS :
        await DM.DiscordManagement.delete_channels(ctx, bot_discord, "commande-annulee")
    else :
        await ctx.send("Vous n'êtes pas autorisé à effectuer cette commande !")

@bot_discord.command(name='editer_annonce')
async def set_annonce(ctx) -> None:
    """
    Editer l'annonce telegram    Usage: !editer_annonce [message]
    """

    if ctx.author.id in AUTHORIZED_DISCORD_USERS :
        content = await DM.DiscordManagement.get_everything_but_discord_commands(ctx, "Veuillez fournir le contenu de l\'annonce.")

        if content != 0 : # Si le message est correct sinon envoie le message d'erreur
            AnnouncementJson.set_json_variable("announce_message", content)
            await ctx.send(f'Annonce définie : {content}')
    else :
        await ctx.send("Vous n'êtes pas autorisé à effectuer cette commande !")

@bot_discord.command(name='facture')
async def invoice(ctx) -> None:

    """
    Créer une facture client.
    """
    if ctx.author.id in AUTHORIZED_DISCORD_USERS or ctx.author.id == CommandJson.search_command_json_variable(None, None, ctx.channel, "cooker_id") :
            username, user_id = FileManagement.get_username_userid_from_channel_name(ctx.channel.name)
            if CommandJson.set_command_json_facture_message(username, user_id, None) : # Revoir la fonction si personnalisation du message demandé
                await ctx.send("Vous avez créé votre facture.")
            else :
                await ctx.send("Votre commande est introuvable !")
    else :
        await ctx.send("Vous n'êtes pas autorisé à effectuer cette commande !")

@bot_discord.command(name='fermer_commande')
async def close_command(ctx) -> None:
    """
    Fermer la commande lorsque le client a été livré.
    """    # Nouvelle variable command_json cooker_name
    # On vérifie si l'admin ou le cooker_name effectue la commande

    if ctx.author.id in AUTHORIZED_DISCORD_USERS or ctx.author.id == CommandJson.search_command_json_variable(None, None, ctx.channel, "cooker_id") :

        username, user_id = FileManagement.get_username_userid_from_channel_name(ctx.channel.name)
        if username is not None and user_id is not None : # Si le channel à l'origine est le bon channel
            command_data = CommandJson.get_command_json(username, user_id, None)

            if command_data is not None : # Si le fichier json de la commande est toujours présent

                await ctx.channel.edit(name="commande-fermee") # Modification du nom du salon
                LoyaltyJson.add_a_point(username, user_id)   # Mise à jour des données de fidélité
                StatsJson.add_a_command()                    # Plus 1 au nombre de commandes total
                StatsJson.update_total_money(command_data.get("price"))

                FileManagement.remove_command_files(username, user_id) # Suppression fichier de la commande
                await DM.DiscordManagement.set_channel_to_view_only_for_member(ctx.channel, ctx.author)

            else :
                print("Le fichier est introuvable : fermer_commande()")
        else:
            print("Commande effectuer dans le mauvais channel : fermer_commande()")
            await ctx.send("Ce n'est pas le bon channel. Effectuer la commande dans le channel de la commande.")
    else :
        await ctx.send("Vous n'êtes pas autorisé à effectuer cette commande !")

@bot_discord.command(name='points')
# La récupération d'une variable fonctionne
async def points(ctx) -> None:
    """
    Permet de voir les points de fidelité d'un utilisateur.
    Usage: !points [username]
    """
    content = await DM.DiscordManagement.get_everything_but_discord_commands(ctx, "Veuillez fournir l'username.")
    username_formated = FileManagement.format_username(content)
    points = LoyaltyJson.get_points_user(username_formated)

    embed_leaderboard = EC.EmbedCommand(ctx, None)
    await embed_leaderboard.send_embed_points(username_formated, points)

@bot_discord.command(name='classement')
async def leaderboard(ctx) -> None:
    """
    Affiche le top 10 des personnes ayant le plus de point de fidelité.
    """

    embed_leaderboard = EC.EmbedCommand(ctx, None)
    await embed_leaderboard.send_embed_leaderboard()

@bot_discord.command(name='stats')
async def show_stats(ctx) -> None:
    """
    Affiche les statistiques total des commandes.
    """
    embed_stats = EC.EmbedCommand(ctx, None)
    await embed_stats.send_embed_stats()

@bot_discord.command(name='help')
async def help(ctx) -> None:
    """
    Affiche toutes les commandes disponible sur le bot discord.
    """
    embed_help = EC.EmbedCommand(ctx, None)
    await embed_help.send_embed_help(bot_discord)

# EVENTS
@bot_discord.event
async def on_message(message) -> None:
    # Ne vérfier que les message d'utilisateur
    # Ne pas vérifier les message précédé de ! pour éviter les commandes.
    if not (message.author == bot_discord.user) and not message.content.startswith('!'):

        # Instant_messaging doit-être actif dans cette conversation.
        if CommandJson.search_command_json_variable(None, None, message.channel.name, "instant_messaging"):

            message_to_send = "Envoyé depuis Discord par "+message.author.name+" : " + message.content

            # Ajout à la queue des messages discord reçu. L'user_id pour l'envoyer à la bonne conversation avec le bot.
            destinataire = FileManagement.get_userid_from_channel_name(message.channel.name)
            queue_bots.get_queue_discord().put((message.channel.name, destinataire, message_to_send))

    await bot_discord.process_commands(message)  # on_message récupère tout les messages. Si c'est une commande !exemple, il faut qu'elle puisse être traiter.

@bot_discord.event
async def on_ready() -> None:
    print(f'Logged in as {bot_discord.user.name} - {bot_discord.user.id}')
    asyncio.create_task(asyncio_taks())         # Démarre les deux tâches check_for_tickets et check_messages

def run_discord_bot(queue_bots_param) -> None:
    global queue_bots                   # Fait en sorte que les queue soit utilisage partout sans passage de paramètre
    queue_bots = queue_bots_param
    bot_discord.run(DISCORD_TOKEN)      # Démrage du bot discord
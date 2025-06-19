"""
Bot Telegram pour la gestion des commandes de livraison.
Ce module gère les interactions avec les utilisateurs via Telegram,
incluant les commandes, les boutons interactifs et la gestion des photos.
"""

import os
from queue import Empty
import asyncio
import threading

# Telegram
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Globals
from utils.constants import TELEGRAM_BOT_TOKEN, AUTHORIZED_TELEGRAM_USERS

# Fonctions statiques
from bots.utils.telegram_management import TelegramManagement
from utils.file_management import FileManagement

from json_processor.blacklist_json import BlacklistJson
from json_processor.command_json import CommandJson
import json_processor.announcement_json  as AJ

# Interfaces
from interfaces.buttons_telegram import ButtonTelegram

# États pour la conversation de prise de commande
ORDER_PHOTO, ORDER_ADDRESS, ORDER_PRICE = range(3)
bot_telegram_api = None

# Commandes Telegram (/nom_commande)
def start(update: Update, context: CallbackContext) -> None:
    """Commande de démarrage pour accueillir les nouveaux utilisateurs."""
    update.message.reply_text(
        f'Pour commencer à recevoir des annonces de livraison de nourriture à pas chère : /start \n\n'+\
        f'Lorsqu\'une annonce s\'affiche, appuyez sur \"Order\" pour commander ou alors \"Vouch\" pour vérifier les faits.\n\n'+\
        f'Envie de commander ? Vous devrez envoyer la photo de votre commande dans la conversation comme preuve puis votre adresse et enfin le prix.\n\n'+\
        f'Pour annuler votre commande : /annuler_commande'
    ) # Envoie d'un texte au démarage de la conversation avec le bot

def test(update, context) -> None:
    update.message.reply_text("Test réussi ! Telegram")

def announce(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id in AUTHORIZED_TELEGRAM_USERS :
        annonce = AJ.AnnouncementJson.search_json_variable("announce_message")                      # Récupération du texte de l'annonce
        Btn_Telegram = ButtonTelegram()
        reply_markup = Btn_Telegram.get_button_order_proof()                                     # Création et récupération des boutons
        TelegramManagement.send_message_to_all_users(context, annonce, reply_markup) # Envoie un message à tout les utilisateurs ayant une conversation avec le bot telegram

    else:
        update.message.reply_text("Vous n'êtes pas autorisé à utiliser cette commande.")

def cancel_command(update: Update, context: CallbackContext) -> None:
    success_command_etat = CommandJson.set_command_json_variable(update.effective_user.full_name, update.effective_user.id, None, "command_etat", 1) # Mise en suppression
    if success_command_etat :
        CommandJson.set_command_json_variable(update.effective_user.full_name, update.effective_user.id, None, "instant_messaging", 0) # Arrêt du système de conversation instannée

        update.message.reply_text("Commande annulé. Veuillez attendre 2min avant de recréer votre commande.")
    else :
        print("Erreur, la commande n'existe pas")
        update.message.reply_text("Tu n'as pas de commande en cours.")

def invoice(update: Update, context: CallbackContext) -> None:
    try:
        facture_message = CommandJson.search_command_json_variable(update.effective_user.full_name, update.effective_user.id, None, "facture_message")
        update.message.reply_text(facture_message)
    except:
        update.message.reply_text("Aucune facture n'a encore été ajouté à votre commande")

# Trigger lorsqu'il y a un CallbackQueryHandler qui ici est un clique sur l'embed de notre annonce
def bouton_click(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    query.answer() # Valide le fait que la requête à été traité.
    action, unique_id = query.data.split('-')

    if unique_id == AJ.AnnouncementJson.search_json_variable("last_announce_id"): # Est-ce la dernière annonce telegram ?

        json_file_path = FileManagement.get_command_json_path(update.effective_user.full_name, update.effective_user.id)

        if not os.path.exists(json_file_path): # Le fichier Command .json existe-il déjà ?

            if action == "order": # Le bouton cliqué est-il "commander" ?

                if not BlacklistJson.is_userid_in_blacklist(update.effective_user.id) : # Si l'utilisateur n'est pas dans la blacklist

                    context.user_data["state"] = ORDER_PHOTO # Lancement du système de questionnaire pour la commande
                    query.message.reply_text("Envoyez la photo de votre commande:")

                else :
                    query.message.reply_text("Désolé, vous n'êtes pas autorisé à passer une commande.")

            elif action == "proof": # Le bouton cliqué est-il "preuves" ?

                # Lien vers le groupe tegram privées permettant de consulter les preuves
                query.message.reply_text(f"Voici le groupe ou vous pouvez avoir les preuves de notre travail: https://t.me/joinchat/https://t.me/+Nl5gbPuTSqk0MGE0")

        else :
            query.message.reply_text("Vous avez déjà une commande en traitement.")

    else:
        query.message.reply_text("Cette annonce est expirée.")

# Trigger on_message ou photo dans la conversation telegram
def command(update: Update, context: CallbackContext) -> None:

    state = context.user_data.get("state", None)

    if state == ORDER_PHOTO:
        photo = update.message.photo[-1].file_id
        context.user_data["order_photo"] = photo

        # Etape suivante
        context.user_data["state"] = ORDER_ADDRESS
        update.message.reply_text("Donnez votre adresse:")

    elif state == ORDER_ADDRESS:
        address = update.message.text
        context.user_data["order_address"] = address

        # Etape suivante
        context.user_data["state"] = ORDER_PRICE
        update.message.reply_text("Donnez le prix de votre commande:")

    elif state == ORDER_PRICE:
        price = update.message.text
        context.user_data["order_price"] = price

        # Gestion de la photo
        photo_id = context.user_data["order_photo"]
        photo_file = context.bot.get_file(photo_id)

        username = FileManagement.format_username(update.effective_user.full_name)
        photo_path = FileManagement.get_command_jpg_path(username)
        photo_file.download(photo_path)

        # Fichier JSON sauvegarde
        command_channel_name = FileManagement.get_command_channel_name(update.effective_user.full_name, update.effective_user.id)

        user_data = {
            "user_id": update.effective_user.id,
            "username": username,
            "address": context.user_data["order_address"],
            "price": context.user_data["order_price"],
            "photo_path": photo_path,
            "cooker_id": 0,
            "facture_message": "",
            "instant_messaging": 0,
            "ticket_etat": 0,
            "command_etat": 0
        }

        CommandJson.save_command_json(None, None, command_channel_name, user_data)

        # Reset des champs de commande dans le bot telegram
        # context.user_data.pop("state", None)
        context.user_data.pop("order_photo", None)
        context.user_data.pop("order_address", None)
        context.user_data.pop("order_price", None)
        context.user_data.pop("state", None)

        update.message.reply_text("Merci pour votre commande !")


    # Instant messagging
    origine = FileManagement.get_command_channel_name(update.effective_user.full_name, update.effective_user.id)

    if CommandJson.search_command_json_variable(None, None, origine, "instant_messaging"): # Vérifie que la conversation instantané est en cours
        send_to_discord(update, origine)

# Gestion de l'instant messaging
async def async_check_messages() -> None:
    while True:
        try:
            channel_name, destinataire, message = queue_bots.get_queue_discord().get(timeout=0.5)

            if CommandJson.search_command_json_variable(None, None, channel_name, "instant_messaging"):

                bot_telegram_api.send_message(chat_id=destinataire, text=message)

        except Empty:
            pass # Rien à faire si la file d'attente est vide
        await asyncio.sleep(1)  # attendre 1 seconde

def run_async_check_messages() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_check_messages())

def send_to_discord(update, origine) -> None:

    if not update.message.text.startswith('/'): # AttributeError: 'NoneType' object has no attribute 'startswith'

        message = "Envoyé depuis Telegram par "+update.effective_user.full_name+" : " + update.message.text

        queue_bots.get_queue_telegram().put((origine, message))

def main() -> None:

    # Déclaration du bot telegram
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Déclaration des commandes télégram, paramètre de gauche /paramètre1 dans telegram puis apelle fonction du paramètre de droite
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('annonce', announce))
    dispatcher.add_handler(CommandHandler('annuler_commande', cancel_command))
    dispatcher.add_handler(CommandHandler('facture', invoice))
    updater.dispatcher.add_handler(CommandHandler('test', test))

    # Triggers
    dispatcher.add_handler(CallbackQueryHandler(bouton_click))

    # Si message ou photo appelé command
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, command))
    dispatcher.add_handler(MessageHandler(Filters.photo, command))

    thread = threading.Thread(target=run_async_check_messages, name="telegram_check_messages")
    thread.start()

    updater.start_polling() # Démarrage telegram bot

def run_telegram_bot(queue_bots_param) -> None:
    global bot_telegram_api
    global queue_bots

    bot_telegram_api = Bot(token=TELEGRAM_BOT_TOKEN) # Variable API en direct
    queue_bots = queue_bots_param                         # Les queues bots pour la gestion des messages via une file
    main()

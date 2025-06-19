
class TelegramManagement():

    def send_message_to_all_users(context, text, buttons) -> bool:
        sucess = True
        try :
            for user_id in context.dispatcher.user_data:
                context.bot.send_message(chat_id=user_id, text=text, reply_markup=buttons)
        except :
            sucess = False

        return sucess

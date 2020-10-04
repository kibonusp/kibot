from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import random
import os

def webabraco(update, context):    
    gif = "./Amor/Abraco/"
    gif += random.choice(os.listdir(gif))
    
    hugged = update.message.text.partition(' ')[2]
    username = update.effective_user.username 

    if hugged:
        message = f"{hugged}, @{username} te deu um abracinho (つ≧▽≦)つ"
        context.bot.send_animation(chat_id=update.message.chat.id, animation=open(gif, "rb"), caption=message)
    else:
        message = f"@{usename}, parece que você não vai dar um abracinho hj ʕ´• ᴥ•̥`ʔ"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def webbeijo(update, context):
    gif = "./Amor/Beijo/"
    gif += random.choice(os.listdir(gif))
    
    kissed = update.message.text.partition(' ')[2]
    username = update.effective_user.username

    if kissed:
        message = f"{kissed}, @{username} te deu um beijinho (づ￣ ³￣)づ"
        context.bot.send_animation(chat_id=update.message.chat.id, animation=open(gif, "rb"), caption=message)
    else:
        message = f"@{username}, parece que você não vai dar um beijinho hj ʕ´• ᴥ•̥`ʔ"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def webcafune(update, context):
    gif = "./Amor/Cafune/"
    gif += random.choice(os.listdir(gif))
    
    petted = update.message.text.partition(' ')[2]
    username = update.effective_user.username

    if petted:
        message = f"{petted}, @{username} te fez um cafuné (｡･ω･｡)ﾉ♡"
        context.bot.send_animation(chat_id=update.message.chat.id, animation=open(gif, "rb"), caption=message)
    else:
        message = f"@{username}, parece que você não vai fazer cafuné hj ʕ´• ᴥ•̥`ʔ"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def websexo(update, context):
    eaten = update.message.text.partition(' ')[2]
    eater = update.effective_user.username

    if eaten:
        response = [f"{eaten}: Já volto ><",
        f"@{eater}: lava a bunda direito",
        f"{eaten}: Lavei",
        f"{eaten}: ><",
        f"@{eater}: deixa eu ver",
        f"{eaten}: *viro a bundinha pro ga*",
        f"@{eater}: *dou uma lambida*",
        f"{eaten}: OOOHH YEAAAH",
        f"{eaten}: >//////<",
        f"@{eater}: TA SUJO😡 ",
        f"{eaten}: NÃO TÁ😭 "]
    else:
        response = [f"@{username}, você precisa dizer quem você quer comer ^^"]
    
    for message in response:
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            sleep(1.5)
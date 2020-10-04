from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
from webcommands import webabraco, webbeijo, webcafune, websexo
from databaseManager import DatabaseManager
from informacoes import TOKEN
from dentes import dente_fotos
from time import sleep
import logging
import random
import os

SENT_IMAGES = set()
DATABASE_URL = os.environ['DATABASE_URL']
MBTILIST = ["ENFJ", "INFJ", "INTJ", "ENTJ", "ENFP", "INFP", "INTP", "ENTP", "ESFP", "ISFP", "ISTP", "ESTP", "ESFJ", "ISFJ", "ISTJ", "ESTJ"]
DBM = DatabaseManager(DATABASE_URL)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Oi, que casada você vai querer comer hoje?")

def mbti(update, context):
    mbti = update.message.text.partition(' ')[2].upper()
    username = update.effective_user.name
    user_id = update.effective_user.id

    if mbti in MBTILIST:
        if not DBM.is_user_registered(username, user_id):
            DBM.register_new_user(username, user_id)

        DBM.set_mbti_value(mbti, user_id)
        response = f"MBTI de @{username} configurado para {mbti}."
    else:
        response = f"Digite uma personalidade MBTI válida, @{username}."
    
    context.bot.sendMessage(chat_id=update.effective_chat.id, tex=response)

def casal_mbti(update, context):
    response = list()
    username = update.effective_user.username
    user_id = update.effective_user.id

    companions = DBM.find_mbti_couples(response, username, user_id)
    for text in response:
        context.bot.send_message(chat_id=update.effective_chat.id,text=text)
    
    return companions

def casalpossivel(update, context):
    companions = casal_mbti(update, context)
    username = update.effective_user.username

    if companions:
        response = ["Lista de Companheiros:"]
        for companion in companions:
            response.append(f"{companion}")
    else:
        response = f"Não há companheiros disponíveis para @{username}"

    context.bot.send_message(chat_id=update.effective_chat.id, text="\n\t".join(response))

def parceiro_mbti(update, context):
    companions = casal_mbti(update, context)
    username = update.effective_user.username

    if companions:
        companion = random.choice(companions)
        response = f"O companheiro ideal do(a) @{username} é: @{companion}"
    else:
        response = f"Não hácompanheiros disponíveis para @{username}."

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def furry(update, context):
    image_path = "./Furry Images/"
    image_path += random.choice(os.listdir(image_path))
    context.bot.sendPhoto (chat_id=update.message.chat_id, photo=open(image_path, 'rb'))

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def dividegrupos(update, context):
    people = update.message.text.partition(' ')[2].split(' ')
    if people == ['']:
        response = ["Por favor, passe os argumentos adequadamente. Para dúvidas, utilize o comando help."]
    else:
        try:
            group_len = int(people[len(people)-1])
            group_len = int(people[len(people)-1])
            people.pop()
            if group_len <= 0 or group_len > len(people):
                response = ["Escolha um tamanho valido"]
            else:
                random.shuffle(people)
                groups_list = list(chunks(people, group_len))
                response = ["Grupos:"]
                for index, group in enumerate(groups_list):
                        response.append(f"\tGrupo {index}: ")
                        response[index+1] += " ".join(group)
        except:
            response = ["Escolha um tamanho de grupo."]

    context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(response))

def audio(update, context):
    audio = "./Audios/"
    audio += random.choice(os.listdir(audio))
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio, 'rb'))

def ping(update, context):
    ping = "./Ping Pong/ping.ogg"
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(ping, 'rb'))

def pong(update, context):
    pong = "./Ping Pong/pong.ogg"
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(pong, 'rb'))

def cancelado(update, context):
    cancelado = update.message.text.partition(' ')[2]
    if not cancelado:
        response = "@{}, se você continuar errando os comandos vou ter que te cancelar \U0000274C \U0000274C \U0001F621".format(update.effective_user.username)
    elif "kibon" in cancelado or "Gabriel" in cancelado or "Freitas" in cancelado or "Furry" in cancelado or "casada" in cancelado or "comedor" in cancelado:
        response = "PAROU PAROU!!!!!. Primeira lei da robótica aqui, amigo. Um robô não pode cancelar seu criador \U0001F47E"
    else:
        response =  "Oopa opa amigo \U0001f645\U0001f645 {} \U0000270B\U0000270B pare por aí \U000026A0\U000026A0 parece que vc foi \U0000274C cancelado \U0000274C".format(cancelado)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        
def dente(update, context):
    photo_path = "./Odontologia/"

    while True:
        print(SENT_IMAGES)
        photo = random.choice(list(dente_fotos.keys()))
        if len(SENT_IMAGES) == len(dente_fotos.keys()):
            print("imhre")
            SENT_IMAGES.clear()
        if photo not in SENT_IMAGES:
            SENT_IMAGES.add(photo)
            break
   
    is_audio = False 
    if photo == "suga" or photo == "motorzim":
        audio_path = "./Audio-dente/"
        audio_path += random.choice(list(dente_fotos[photo]["audio"].values()))
        is_audio = True
    
    photo_path += dente_fotos[photo]["arquivo"]
    legenda = dente_fotos[photo]["legenda"]

    context.bot.sendPhoto(chat_id = update.message.chat_id, photo = open(photo_path, "rb"), caption = legenda, parse_mode = "html")
    
    if is_audio:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio_path, 'rb'))

def ajuda(update, context):
    response = ["start - /start", "mbti - /mbti [MBTI]", "casais - /casais",
                "parceiro - /parceiro", "furry - /furry", "dividegrupos - /dividegrupos [PESSOA1] [PESSOA 2] ... [TAMANHO_DO_GRUPO]","audio - /audio", "help - /help",
                "ping - /ping", "pong - /pong", "pingpong - /pingpong [PESSOA1] [PESSOA2]",
                "cancelado - /cancelado [NOME]", "webcafune - /webcafune [PESSOA]",
                "webabraco - /webabraco [PESSOA]", "webbeijo - /webbeijo [PESSOA]",
                "websexo - /websexo [PESSOA]", "dente - /dente"]

    context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(response))

def main():
    PORT = int(os.environ.get('PORT', 5000))
    
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('mbti', mbti))
    dp.add_handler(CommandHandler('casais', casalpossivel))
    dp.add_handler(CommandHandler('parceiro', parceiro_mbti))
    dp.add_handler(CommandHandler('furry', furry))
    dp.add_handler(CommandHandler('dividegrupos', dividegrupos))
    dp.add_handler(CommandHandler('audio', audio))
    dp.add_handler(CommandHandler('help', ajuda))
    dp.add_handler(CommandHandler('ping', ping))
    dp.add_handler(CommandHandler('pong', pong))
    dp.add_handler(CommandHandler('cancelado', cancelado))
    dp.add_handler(CommandHandler('webabraco', webabraco))
    dp.add_handler(CommandHandler('webbeijo', webbeijo))
    dp.add_handler(CommandHandler('websexo', websexo))
    dp.add_handler(CommandHandler('webcafune', webcafune))
    dp.add_handler(CommandHandler('dente', dente))
    
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook(APPNAME + TOKEN)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("Digite Ctrl + C para desativar.")
    print("=== BOT ATIVADO ===")
    main()
    print("=== BOT DESATIVADO ===")



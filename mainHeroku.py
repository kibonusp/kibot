from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import logging
import random
from databaseManager import DBM
import os
from informacoes import TOKEN, APPNAME

DATABASE_URL = os.environ['DATABASE_URL']
MBTILIST = ["ENFJ", "INFJ", "INTJ", "ENTJ", "ENFP", "INFP", "INTP", "ENTP", "ESFP", "ISFP", "ISTP", "ESTP", "ESFJ", "ISFJ", "ISTJ", "ESTJ"]
dbm = DBM(DATABASE_URL)
LISTAABRACO = []

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Oi, que casada você vai querer comer hoje?")

def mbti(update, context):
    mbtiValue = update.message.text.partition(' ')[2].upper()

    if mbtiValue in MBTILIST:
        dbm.createOrFindUser(update.effective_user.username, update.effective_user.id)
        dbm.setMbtiValue(mbtiValue, update.effective_user.id)
        answerText = "MBTI de @{} configurado para {}.".format(update.effective_user.username, mbtiValue)
        print(answerText)
        context.bot.send_message(chat_id=update.effective_chat.id, text=answerText)

    else:
        answerText = "Digite uma personalidade MBTI válida, @{}.".format(update.effective_user.username)
        context.bot.send_message(chat_id=update.effective_chat.id, text=answerText)

def casalMBTI(update, context):
    response = list()
    companions = dbm.findMbtiCouples(response, update.effective_user.username, update.effective_user.id)
    
    for text in response:
        context.bot.send_message(chat_id=update.effective_chat.id,text=text)
  
    return companions

def casalpossivel(update, context):
    companions = casalMBTI(update, context)
    if companions:
            companionList = "Lista de Companheiros:"
            for companion in companions:
                companionList += "\n\t{}".format(companion)
            context.bot.send_message(chat_id=update.effective_chat.id, text=companionList)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Não há companheiros disponíveis para @{}.".format(update.effective_user.username))

def parceiroMBTI(update, context):
    companions = casalMBTI(update, context)
    if companions:
            companion = random.choice(companions)
            context.bot.send_message(chat_id=update.effective_chat.id, text="O companheiro ideal do(a) @{} é: @{}.".format(update.effective_user.username, companion))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Não há companheiros disponíveis para @{}.".format(update.effective_user.username))

def furry (update, context):
    image = "./Furry Images/"
    image += random.choice(os.listdir(image))
    context.bot.sendPhoto (chat_id=update.message.chat_id, photo=open(image, 'rb'))

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def dividegrupos (update, context):
    listaPessoas = update.message.text.partition(' ')[2].split(' ')
    if listaPessoas == ['']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, passe os argumentos adequadamente. Para dúvidas, utilize o comando help.")
    else:
        try:
            tamanhoGrupo = int(listaPessoas[len(listaPessoas)-1])
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Escolha um tamanho de grupo.")
            return
        listaPessoas.pop()
        random.shuffle(listaPessoas)
        if tamanhoGrupo <= 0 or tamanhoGrupo > len(listaPessoas):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Escolha um tamanho de grupo válido.")
        else:
            listaGrupos = list(chunks(listaPessoas, tamanhoGrupo))
            mensagem = "Grupos:\n"
            for posGrupo, grupo in enumerate(listaGrupos):
                mensagem += "\tGrupo {}:".format(posGrupo)
                for integrante in grupo:
                    mensagem += " "+integrante
                mensagem += '\n'
            context.bot.send_message(chat_id=update.effective_chat.id, text=mensagem)

def audio (update, context):
    audio = "./Audios/"
    audio += random.choice(os.listdir(audio))
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio, 'rb'))

def ping (update, context):
    ping = "./Ping Pong/ping.mp3"
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(ping, 'rb'))

def pong (update, context):
    pong = "./Ping Pong/pong.mp3"
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(pong, 'rb'))

def cancelado (update, context):
    cancelado = update.message.text.partition(' ')[2]
    if cancelado == "":
        message = "@{}, se você continuar errando os comandos vou ter que te cancelar \U0000274C \U0000274C \U0001F621".format(update.effective_user.username)
    elif "kibon" in cancelado or "Gabriel" in cancelado or "Freitas" in cancelado or "Furry" in cancelado or "casada" in cancelado or "comedor" in cancelado:
        message = "PAROU PAROU!!!!!. Primeira lei da robótica aqui, amigo. Um robô não pode cancelar seu criador \U0001F47E"
    else:
        message =  "Oopa opa amigo \U0001f645\U0001f645 {} \U0000270B\U0000270B pare por aí \U000026A0\U000026A0 parece que vc foi \U0000274C cancelado \U0000274C".format(cancelado)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def ajuda (update, context):
    helpText = '''start - /start
mbti - /mbti [MBTI]
casais - /casais
parceiro - /parceiro
furry - /furry
dividegrupos - /dividegrupos [PESSOA1] [PESSOA 2] ... [TAMANHO_DO_GRUPO]
audio - /audio
help - /help
ping - /ping
pong - /pong
cancelado - /cancelado [NOME]'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=helpText)

def webabraco (update, context):    # webabraco @sorvete
    abracado = update.message.text.partition(' ')[2]
    confirm = "@{}, @{} te deu um abracinho (つ≧▽≦)つ".format(abracado, update.effective_user.username)
    context.bot.send_message(chat_id=update.effective_chat.id, text=confirm)
    context.bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
    context.bot.sendDocument(chat_id=chat_id, document="./Amor/abraco.gif.mp4")

def webbeijo

def main():
    PORT = int(os.environ.get('PORT', 5000))
    
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('mbti', mbti))
    dp.add_handler(CommandHandler('casais', casalpossivel))
    dp.add_handler(CommandHandler('parceiro', parceiroMBTI))
    dp.add_handler(CommandHandler('furry', furry))
    dp.add_handler(CommandHandler('dividegrupos', dividegrupos))
    dp.add_handler(CommandHandler('audio', audio))
    dp.add_handler(CommandHandler('help', ajuda))
    dp.add_handler(CommandHandler('ping', ping))
    dp.add_handler(CommandHandler('pong', pong))
    dp.add_handler(CommandHandler('cancelado', cancelado))
    dp.add_handler(CommandHandler('webabraco', webabraco))

    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook(APPNAME + TOKEN)
    updater.idle()

if __name__ == '__main__':
    print("Digite Ctrl + C para desativar.")
    print("=== BOT ATIVADO ===")
    main()
    print("=== BOT DESATIVADO ===")
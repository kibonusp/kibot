from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import logging
import random
import psycopg2
import os

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Oi, que casada você vai querer comer hoje?")
    print("Oi, que casada você vai querer comer hoje?")

def createOrFindUser (username, userID, DATABASE_URL):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    cur.execute("SELECT username FROM Users WHERE id = (%s)", (userID,))
    userTuple = cur.fetchall()
    try:
        Username = list(userTuple[0])[0]
        userAchado = 1
    except:
        Username = username
        userAchado = 0
    if userAchado == 0:
        cur.execute("INSERT INTO Users(id, username) VALUES (%s, %s)", (userID, username))
        print("Usuário novo adicionado: {}".format(username))
    else:
        print("Usuário encontrado: {}".format(username))
    print("userID:", userID)
    conn.commit()

def mbti(update, context, mbtiList, DATABASE_URL):
    mbtiValue = update.message.text.partition(' ')[2].upper()

    if mbtiValue in mbtiList:
        createOrFindUser(update.effective_user.username, update.effective_user.id, DATABASE_URL)
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute("UPDATE Users SET mbti=(%s) WHERE id=(%s)", (mbtiValue, update.effective_user.id))
        answerText = "MBTI de @{} configurado para {}.".format(update.effective_user.username, mbtiValue)
        context.bot.send_message(chat_id=update.effective_chat.id, text=answerText)
        conn.commit()

    else:
        answerText = "Digite uma personalidade MBTI válida, @{}.".format(update.effective_user.username)
        context.bot.send_message(chat_id=update.effective_chat.id, text=answerText)

def casalMBTI (update, context, DATABASE_URL):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()

    casais = {"ESTJ": "ISFP", "ISFP":"ESTJ",
            "ISTJ": "ESFP", "ISTJ":"ESFP",
            "INFP": "ENFJ", "ENFJ":"INFP",
            "INTP": "ENTJ", "ENTJ": "INTP",
            "ESTP": "ISFJ", "ISFJ": "ESTP",
            "ENTP": "INFJ", "INFJ": "ENTP",
            "ESFJ": "ISTP", "ISTP": "ESFJ",
            "ENFP": "INTJ", "INTJ": "ENFP"}
    try:  
        cur.execute("SELECT mbti FROM Users WHERE id=(%s)", (update.effective_user.id,))
        userTuple = cur.fetchall()
        userMBTI = list(userTuple[0])[0]
    except:
        print("Usuário @{} não cadastrado".format(update.effective_user.username))
        context.bot.send_message(chat_id=update.effective_chat.id, text="@{}, defina sua personalidade MBTI antes com o comando mbti.".format(update.effective_user.username))
        companions = [0]

    try:
        cur.execute("SELECT username FROM Users WHERE mbti=(%s)", (casais[userMBTI],))
        userTuple = cur.fetchall()
        companions = list(userTuple[0])
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Não há companheiros disponíveis para @{}.".format(update.effective_user.username))
        companions = [0]
    conn.commit()
    return companions

def casalpossivel (update, context, mbtiList, DATABASE_URL):
    companions = casalMBTI(update, context, DATABASE_URL)
    if companions[0] != 0:
        companionList = "Lista de Companheiros:\n"
        for companion in companions:
            companionList += "\t{}".format(companion)
        context.bot.send_message(chat_id=update.effective_chat.id, text=companionList)


def parceiroMBTI (update, context, mbtiList, DATABASE_URL):
    companions = casalMBTI(update, context, DATABASE_URL)
    if companions[0] != 0:
        companion = random.choice(companions)
        context.bot.send_message(chat_id=update.effective_chat.id, text="O companheiro ideal do(a) @{} é: @{}.".format(update.effective_user.username, companion))

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

def main():
    DATABASE_URL = os.environ['DATABASE_URL']

    mbtiList = ["ENFJ", "INFJ", "INTJ", "ENTJ", "ENFP", "INFP", "INTP", "ENTP", "ESFP", "ISFP", "ISTP", "ESTP", "ESFJ", "ISFJ", "ISTJ", "ESTJ"]

    PORT = int(os.environ.get('PORT', 5000))
    TOKEN = None
    with open("token.txt") as f:
        TOKEN = f.read().strip()
    
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('mbti', lambda bot, update: mbti(bot, update, mbtiList, DATABASE_URL)))
    dp.add_handler(CommandHandler('casais', lambda bot, update: casalpossivel(bot, update, mbtiList, DATABASE_URL)))
    dp.add_handler(CommandHandler('parceiro', lambda bot, update: parceiroMBTI(bot, update, mbtiList, DATABASE_URL)))
    dp.add_handler(CommandHandler('furry', furry))
    dp.add_handler(CommandHandler('dividegrupos', dividegrupos))
    dp.add_handler(CommandHandler('audio', audio))
    dp.add_handler(CommandHandler('help', ajuda))
    dp.add_handler(CommandHandler('ping', ping))
    dp.add_handler(CommandHandler('pong', pong))
    dp.add_handler(CommandHandler('cancelado', cancelado))

    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook('https://pure-hollows-28450.herokuapp.com/' + TOKEN)
    updater.idle()

if __name__ == '__main__':
    print("Digite Ctrl + C para desativar.")
    print("=== BOT ATIVADO ===")
    main()
    print("=== BOT DESATIVADO ===")
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import logging
import sqlite3
import random
import os

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Oi, que casada você vai querer comer hoje?")
    print("Oi, que casada você vai querer comer hoje?")

def createOrFindUser (username, userID):
    conn = sqlite3.connect('userInfo')
    cur = conn.cursor()

    cur.execute("SELECT username FROM User WHERE id = (?)", (userID,))
    userTuple = cur.fetchall()
    try:
        Username = list(userTuple[0])[0]
        userAchado = 1
    except:
        Username = username
        userAchado = 0
    if userAchado == 0:
        cur.execute("INSERT INTO User(id, username) VALUES (?, ?)", (userID, username))
        print("Usuário novo adicionado: {}".format(username))
    else:
        print("Usuário encontrado: {}".format(username))
    print("userID:", userID)
    conn.commit()

def mbti(update, context):
    mbtiValue = update.message.text.partition(' ')[2].upper()
    mbtiList = ["ENFJ", "INFJ", "INTJ", "ENTJ", "ENFP", "INFP", "INTP", "ENTP", "ESFP", "ISFP", "ISTP", "ESTP", "ESFJ", "ISFJ", "ISTJ", "ESTJ"]

    if mbtiValue in mbtiList:
        createOrFindUser(update.effective_user.username, update.effective_user.id)
        conn = sqlite3.connect('userInfo')
        cur = conn.cursor()
        cur.execute("UPDATE User SET mbti=(?) WHERE id=(?)", (mbtiValue, update.effective_user.id))
        answerText = "MBTI de @{} configurado para {}.".format(update.effective_user.username, mbtiValue)
        context.bot.send_message(chat_id=update.effective_chat.id, text=answerText)
        conn.commit()

    else:
        answerText = "Digite uma personalidade MBTI válida, @{}.".format(update.effective_user.username)
        context.bot.send_message(chat_id=update.effective_chat.id, text=answerText)

def casalMBTI (update, context):
    conn = sqlite3.connect('userInfo')
    cur = conn.cursor()

    casais = {"ESTJ": "ISFP", "ISFP":"ESTJ",
            "ISTJ": "ESFP", "ISTJ":"ESFP",
            "INFP": "ENFJ", "ENFJ":"INFP",
            "INTP": "ENTJ", "ENTJ": "INTP",
            "ESTP": "ISFJ", "ISFJ": "ESTP",
            "ENTP": "INFJ", "INFJ": "ENTP",
            "ESFJ": "ISTP", "ISTP": "ESFJ",
            "ENFP": "INTJ", "INTJ": "ENFP"}
    mbtiList = ["ENFJ", "INFJ", "INTJ", "ENTJ", "ENFP", "INFP", "INTP", "ENTP", "ESFP", "ISFP", "ISTP", "ESTP", "ESFJ", "ISFJ", "ISTJ", "ESTJ"]

    cur.execute("SELECT mbti FROM User WHERE id=(?)", (update.effective_user.id,))
    userTuple = cur.fetchall()
    userMBTI = list(userTuple[0])[0]
    if userMBTI not in mbtiList:
        companions= [-1]
    else:
        try:
            cur.execute("SELECT username FROM User WHERE mbti=(?)", (casais[userMBTI],))
            userTuple = cur.fetchall()
            companions = list(userTuple[0])
        except:
            companions = [0]
    conn.commit()
    return companions

def casalpossivel (update, context):
    companions = casalMBTI(update, context)
    if companions[0] == -1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Você precisa definir seu MBTI primeiro")
    elif companions[0] == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Não há companheiros disponíveis.")
    else:
        companionList = "Lista de Companheiros:\n"
        for companion in companions:
            companionList += "\t{}".format(companion)
        context.bot.send_message(chat_id=update.effective_chat.id, text=companionList)


def parceiroMBTI (update, context):
    companions = casalMBTI(update, context)
    if companions[0] == -1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Você precisa definir seu MBTI primeiro")
    if companions[0] == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Não há companheiros disponíveis.")
    else:
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
    tamanhoGrupo = int(listaPessoas[len(listaPessoas)-1])
    listaPessoas.pop()
    random.shuffle(listaPessoas)
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
help - /help'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=helpText)

def ping (update, context):
    ping = "./Ping Pong/ping.mp3"
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(ping, 'rb'))

def pong (update, context):
    pong = "./Ping Pong/pong.mp3"
    context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(pong, 'rb'))

def main():
    PORT = int(os.environ.get('PORT', 5000))
    TOKEN = None
    with open("token.txt") as f:
        TOKEN = f.read().strip()
    
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

    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook('https://pure-hollows-28450.herokuapp.com/' + TOKEN)
    updater.idle()

if __name__ == '__main__':
    print("Digite Ctrl + C para desativar.")
    print("=== BOT ATIVADO ===")
    main()
    print("=== BOT DESATIVADO ===")
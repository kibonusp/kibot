from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import logging
import random
import sqlite3
import os
from dentes import dente_fotos
from informacoes import TOKEN
from time import sleep
# import speech_recognition as sr
import subprocess
import json
import time
from sorvetes import iceCreamImages

DATABASE = "fuvest"
MBTILIST = ["ENFJ", "INFJ", "INTJ", "ENTJ", "ENFP", "INFP", "INTP", "ENTP", "ESFP", "ISFP", "ISTP", "ESTP", "ESFJ", "ISFJ", "ISTJ", "ESTJ"]

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Oi, que casada você vai querer comer hoje?")

def createOrFindUser (username, userID):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT username FROM Users WHERE id = (?)", (userID,))
    user = cur.fetchall()

    if not user:
        cur.execute("INSERT INTO Users(id, username) VALUES     (%s, %s)", (userID, username))
        print("Usuário novo adicionado: {}".format(username))
    else:
        print("Usuário encontrado: {}".format(username))
    print("userID:", userID)
    conn.commit()

def mbti(update, context):
    mbtiValue = update.message.text.partition(' ')[2].upper()

    if mbtiValue in MBTILIST:
        createOrFindUser(update.effective_user.username, update.effective_user.id)
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("UPDATE Users SET mbti=(?) WHERE id=(?)", (mbtiValue, update.effective_user.id))
        conn.commit()
        answerText = "MBTI de @{} configurado para {}.".format(update.effective_user.username, mbtiValue)
        context.bot.send_message(chat_id=update.effective_chat.id, text=answerText)

    else:
        answerText = "Digite uma personalidade MBTI válida, @{}.".format(update.effective_user.username)
        context.bot.send_message(chat_id=update.effective_chat.id, text=answerText)

def casalMBTI (update, context):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    response = list()
    casais = {"ESTJ": "ISFP", "ISFP":"ESTJ",
            "ISTJ": "ESFP", "ESFP":"ISTJ",
            "INFP": "ENFJ", "ENFJ":"INFP",
            "INTP": "ENTJ", "ENTJ": "INTP",
            "ESTP": "ISFJ", "ISFJ": "ESTP",
            "ENTP": "INFJ", "INFJ": "ENTP",
            "ESFJ": "ISTP", "ISTP": "ESFJ",
            "ENFP": "INTJ", "INTJ": "ENFP"}

    cur.execute("SELECT mbti FROM Users WHERE id=(%s)", (update.effective_user.id,))
    userMbtiTuple = cur.fetchall()

    companions = list()
    if not userMbtiTuple:
        print("Usuário @{} não cadastrado".format(update.effective_user.username,))
        response.append("@{}, defina sua personalidade  MBTI antes com o comando mbti.".format(update.effective_user.id,))
        return companions

    userMbti = list(userMbtiTuple[0])[0]
    cur.execute("SELECT username FROM Users WHERE mbti=(%s)", (casais[userMbti],))
    matches = cur.fetchall()
    for user in matches:
        formatedCompanion = ''.join(map(str,user[0]))
        companions.append(formatedCompanion)
    conn.commit()

    for text in response:
        context.bot.send_message(chat_id=update.effective_chat.id,text=text)
    return companions

def casalpossivel (update, context):
    companions = casalMBTI(update, context)
    if companions:
        companionList = "Lista de Companheiros:"
        for companion in companions:
            companionList += "\n\t{}".format(companion)
        context.bot.send_message(chat_id=update.effective_chat.id, text=companionList)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Não há companheiros disponíveis para @{}.".format(update.effective_user.username))

def parceiroMBTI (update, context):
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

def loadJSON(nomeArquivo):
    with open(nomeArquivo, "rb")as arquivo:
        return json.load(arquivo)

def mensagemvitoria(rodadas, vitoriaPartida, vitoriaJogador, listaMensagens):
    if not vitoriaPartida:
        mensagemEnviar = listaMensagens[4]
    elif rodadas <= 3:
        mensagemEnviar = "{}{}".format(listaMensagens[0], vitoriaJogador)
    elif rodadas > 3 and rodadas <= 6:
        mensagemEnviar = "{}{}".format(listaMensagens[1], vitoriaJogador)
    elif rodadas > 6 and rodadas <= 8:
        mensagemEnviar = "{}{}".format(listaMensagens[2], vitoriaJogador)
    else:
        mensagemEnviar = "{}{}".format(listaMensagens[3], vitoriaJogador)
    return mensagemEnviar
        
def pingpong(update, context):
    listaMensagens = loadJSON("ping_pong_mensagens.json")
    listaJogadores = update.message.text.split()[1:]
    if len(listaJogadores) < 2 or len(listaJogadores) > 2:
        mensagemEnviar = listaMensagens[5]
    else:
        defineLados = random.randint(0,1)
        pingJogador = listaJogadores[defineLados]
        pongJogador = listaJogadores[1-defineLados]
        rodadas = 0
        vitoria = False
        while not vitoria and rodadas < 10:
            #round ping
            if not vitoria:
                context.bot.send_audio(chat_id=update.effective_chat.id, audio=open("./Ping Pong/ping.ogg", 'rb'))
                if random.randint(0,10) == 1:
                    vitoria = True
                    vitoriaJogador = pingJogador
            time.sleep(random.uniform(0,1))
            #round pong
            if not vitoria:
                context.bot.send_audio(chat_id=update.effective_chat.id, audio=open("./Ping Pong/pong.ogg", 'rb'))
                if random.randint(0,10) == 1:
                    vitoria = True
                    vitoriaJogador = pongJogador
            time.sleep(random.uniform(0,1))
            rodadas += 2
        mensagemEnviar = mensagemvitoria(rodadas, vitoria, vitoriaJogador, listaMensagens)
    context.bot.send_message(chat_id=update.effective_chat.id, text=mensagemEnviar, reply_to_message_id=update.message.message_id)

def cancelado (update, context):
    cancelado = update.message.text.partition(' ')[2]
    if cancelado == "":
        message = "@{}, se você continuar errando os comandos vou ter que te cancelar \U0000274C \U0000274C \U0001F621".format(update.effective_user.username)
    elif "kibon" in cancelado or "Gabriel" in cancelado or "Freitas" in cancelado or "Furry" in cancelado or "casada" in cancelado or "comedor" in cancelado:
        message = "PAROU PAROU!!!!!. Primeira lei da robótica aqui, amigo. Um robô não pode cancelar seu criador \U0001F47E"
    else:
        message =  "Oopa opa amigo \U0001f645\U0001f645 {} \U0000270B\U0000270B pare por aí \U000026A0\U000026A0 parece que vc foi \U0000274C cancelado \U0000274C".format(cancelado)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def webabraco (update, context):    
    gif = "./Amor/Abraco/"
    gif += random.choice(os.listdir(gif))
    abracado = update.message.text.partition(' ')[2]
    if abracado:
        message = "{}, @{} te deu um abracinho (つ≧▽≦)つ".format(abracado, update.effective_user.username)
        context.bot.send_animation(chat_id=update.message.chat.id, animation=open(gif, "rb"), caption=message)
    else:
        message = "@{}, parece que você não vai dar um abracinho hj ʕ´• ᴥ•̥`ʔ".format(update.effective_user.username)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def webbeijo (update, context):
    gif = "./Amor/Beijo/"
    gif += random.choice(os.listdir(gif))
    beijado = update.message.text.partition(' ')[2]
    if beijado:
        message = "{}, @{} te deu um beijinho (づ￣ ³￣)づ".format(beijado, update.effective_user.username)
        context.bot.send_animation(chat_id=update.message.chat.id, animation=open(gif, "rb"), caption=message)
    else:
        message = "@{}, parece que você não vai dar um beijinho hj ʕ´• ᴥ•̥`ʔ".format(update.effective_user.username)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def webcafune (update, context):
    gif = "./Amor/Cafune/"
    gif += random.choice(os.listdir(gif))
    cafunezado = update.message.text.partition(' ')[2]
    if cafunezado:
        message = "{}, @{} te fez um cafuné (｡･ω･｡)ﾉ♡".format(cafunezado, update.effective_user.username)
        context.bot.send_animation(chat_id=update.message.chat.id, animation=open(gif, "rb"), caption=message)
    else:
        message = "@{}, parece que você não vai fazer cafuné hj ʕ´• ᴥ•̥`ʔ".format(update.effective_user.username)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def websexo (update, context):
    comido = update.message.text.partition(' ')[2]
    if comido:
        comedor = update.effective_user.username
        messages = ["{}: Já volto ><".format(comido),
        "@{}: lava a bunda direito".format(comedor),
        "{}: Lavei".format(comido),
        "{}: ><".format(comido),
        "@{}: deixa eu ver".format(comedor),
        "{}: *viro a bundinha pro ga*".format(comido),
        "@{}: *dou uma lambida*".format(comedor),
        "{}: OOOHH YEAAAH".format(comido),
        "{}: >//////<".format(comido),
        "@{}: TA SUJO😡 ".format(comedor),
        "{}: NÃO TÁ😭 ".format(comido)]
        for message in messages:
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
            sleep(1.5)
    else:
        message = "@{}, você precisa dizer quem você quer comer ^^"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

sent_images = set()
def dente (update, context):
    imagem = "./Odontologia/"
    while True:
        foto = random.choice(list(dente_fotos.keys()))
        if not sent_images.difference(dente_fotos.keys()):
            sent_images.clear()
        if foto not in sent_images:
            sent_images.add(foto)
            break
   
    eh_audio = False 
    
    if foto == "suga" or foto == "motorzim":
        audio = "./Audio-dente/"
        audio += random.choice(list(dente_fotos[foto]["audio"].values()))
        eh_audio = True
    
    imagem += dente_fotos[foto]["arquivo"]
    legenda = dente_fotos[foto]["legenda"]

    context.bot.sendPhoto(chat_id = update.message.chat_id, photo = open(imagem, "rb"), caption = legenda, parse_mode = "html")
    
    if eh_audio:
        context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio, 'rb'))
"""
def traduz (update, context):
    audio  = context.bot.getFile(update.message.reply_to_message.voice)
    ogg = 'audio.ogg'
    wav = 'audio.wav'
    audio.download(ogg)
    process = subprocess.run(['ffmpeg','-i',ogg, wav, '-y'])

    r = sr.Recognizer()
    
    with sr.WavFile(wav) as source:
        with sr.AudioFile(wav) as source:
            voice = r.record(source)
            frase = r.recognize_google(voice, language= 'pt-BR')
            context.bot.send_message(chat_id=update.effective_chat.id, text=frase)
"""

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
pingpong - /pingpong [PESSOA1] [PESSOA2]
cancelado - /cancelado [NOME]
webcafune - /webcafune [PESSOA]
webabraco - /webabraco [PESSOA]
webbeijo - /webbeijo [PESSOA]
websexo - /websexo [PESSOA]
dente - /dente
kibon - /kibon
'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=helpText)

def kibon(update, context):
    image = "./Sorvetes/"
    photo = random.choice(list(iceCreamImages.keys()))
    image += iceCreamImages[photo]["img"]
    caption = "<i>" + iceCreamImages[photo]["cap"] + "</i>"
    context.bot.sendPhoto(chat_id=update.message.chat_id, photo=open(image, "rb"), caption=caption, parse_mode="html")

def main():
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
    dp.add_handler(CommandHandler('pingpong', pingpong))
    dp.add_handler(CommandHandler('cancelado', cancelado))
    dp.add_handler(CommandHandler('webabraco', webabraco))
    dp.add_handler(CommandHandler('webbeijo', webbeijo))
    dp.add_handler(CommandHandler('websexo', websexo))
    dp.add_handler(CommandHandler('webcafune', webcafune))
    dp.add_handler(CommandHandler('dente', dente))
    # dp.add_handler(CommandHandler('traduz', traduz))
    dp.add_handler(CommandHandler('kibon', kibon))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("Digite Ctrl + C para desativar.")
    print("=== BOT ATIVADO ===")
    main()
    print("=== BOT DESATIVADO ===")

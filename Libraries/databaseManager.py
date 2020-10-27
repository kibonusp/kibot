import psycopg2 as psql

class DatabaseManegementPostgres:
    ''' Instance of a Database Manager '''
    def __init__(self, DATABASE_URL):
        self.conn = psql.connect(DATABASE_URL, sslmode='require')
        self.cur = self.conn.cursor()
    
    def createOrFindUser(self, username, userID):
        self.cur.execute("SELECT username FROM Users WHERE id = (%s)", (userID,))
        user = self.cur.fetchall()
        if not user:
            self.cur.execute("INSERT INTO Users(id, username) VALUES     (%s, %s)", (userID, username))
            print("Usuário novo adicionado: {}".format(username))
        else:
            print("Usuário encontrado: {}".format(username))
        print("userID:", userID)
        
        self.conn.commit()
    
    def setMbtiValue(self, mbtiValue, userId):
        self.cur.execute("UPDATE Users SET mbti=(%s) WHERE id=(%s)", (mbtiValue, userId))
        self.conn.commit()
    
    def findMbtiCouples(self, response, username, userId):
        casais = {"ESTJ": "ISFP", "ISFP":"ESTJ",
                "ISTJ": "ESFP", "ESFP":"ISTJ",
                "INFP": "ENFJ", "ENFJ":"INFP",
                "INTP": "ENTJ", "ENTJ": "INTP",
                "ESTP": "ISFJ", "ISFJ": "ESTP",
                "ENTP": "INFJ", "INFJ": "ENTP",
                "ESFJ": "ISTP", "ISTP": "ESFJ",
                "ENFP": "INTJ", "INTJ": "ENFP"}

        self.cur.execute("SELECT mbti FROM Users WHERE id=(%s)", (userId,))
        userMbtiTuple = self.cur.fetchall()

        companions = list()
        if not userMbtiTuple:
            print("Usuário @{} não cadastrado".format(username))
            response.append("@{}, defina sua personalidade  MBTI antes com o comando mbti.".format(username))
            return companions

        userMbti = list(userMbtiTuple[0])[0]
        
        self.cur.execute("SELECT username FROM Users WHERE mbti=(%s)", (casais[userMbti],))

        matches = self.cur.fetchall()

        for user in matches:
            formatedCompanion = ''.join(map(str,user[0]))
            companions.append(formatedCompanion)
        
        self.conn.commit()
        return companions

    def endConnection(self):
        self.conn.commit()
        self.conn.close()   

import sqlite3

class DatabaseManegementSQLite:
    ''' Instance of a Database Manager '''
    def __init__(self, DATABASE):
        self.DATABASE = DATABASE
        pass

    def createOrFindUser(self,username, userID):
        conn = sqlite3.connect(self.DATABASE)
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

    def setMbtiValue(self, mbtiValue, userId):
        conn = sqlite3.connect(self.DATABASE)
        cur = conn.cursor()
        cur.execute("UPDATE Users SET mbti=(?) WHERE id=(?)", (mbtiValue, update.effective_user.id))
        conn.commit()
 
    def findMbtiCouples(self, response, username, userId):
        casais = {"ESTJ": "ISFP", "ISFP":"ESTJ",
                "ISTJ": "ESFP", "ESFP":"ISTJ",
                "INFP": "ENFJ", "ENFJ":"INFP",
                "INTP": "ENTJ", "ENTJ": "INTP",
                "ESTP": "ISFJ", "ISFJ": "ESTP",
                "ENTP": "INFJ", "INFJ": "ENTP",
                "ESFJ": "ISTP", "ISTP": "ESFJ",
                "ENFP": "INTJ", "INTJ": "ENFP"}

        self.cur.execute("SELECT mbti FROM Users WHERE id=(%s)", (userId,))
        userMbtiTuple = self.cur.fetchall()

        companions = list()
        if not userMbtiTuple:
            print("Usuário @{} não cadastrado".format(username))
            response.append("@{}, defina sua personalidade  MBTI antes com o comando mbti.".format(username))
            return companions

        userMbti = list(userMbtiTuple[0])[0]
        
        self.cur.execute("SELECT username FROM Users WHERE mbti=(%s)", (casais[userMbti],))

        matches = self.cur.fetchall()

        for user in matches:
            formatedCompanion = ''.join(map(str,user[0]))
            companions.append(formatedCompanion)
        
        self.conn.commit()
        return companions

    def endConnection(self):
        self.conn.commit()
        self.conn.close()   


"""

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
            companionList += "{}".format(companion)
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

"""
   

import psycopg2 as psql

class DatabaseManager:
    ''' Instance of a Database Manager '''
    def __init__(self, DATABASE_URL):
        self.conn = psql.connect(DATABASE_URL, sslmode='require')
        self.cur = self.conn.cursor()
    
    def is_user_registered(self, username, user_id):
        self.cur.execute("SELECT username FROM Users WHERE id = (%s)", (user_id,))
         
        if not self.cur.fetchall():
            return False
    
        print(f"Usuário encontrado: {username}")
        return True
    
    def register_new_user(self, username, user_id):
        self.cur.execute("INSERT INTO Users(id, username) VALUES     (%s, %s)", (user_id, username))
        print(f"Usuário novo adicionado: {username}")
        self.conn.commit()

    # def createOrFindUser(self, username, userID):
    #     self.cur.execute("SELECT username FROM Users WHERE id = (%s)", (userID,))
    #     user = self.cur.fetchall()
    #     if not user:
    #         self.cur.execute("INSERT INTO Users(id, username) VALUES     (%s, %s)", (userID, username))
    #         print("Usuário novo adicionado: {}".format(username))
    #     else:
    #         print("Usuário encontrado: {}".format(username))
    #     print("userID:", userID)
        
    #     self.conn.commit()
    
    def set_mbti_value(self, mbtiValue, user_id):
        self.cur.execute("UPDATE Users SET mbti=(%s) WHERE id=(%s)", (mbtiValue, user_id))
        self.conn.commit()
    
    def find_mbti_couples(self, response, username, user_id):
        self.cur.execute("SELECT mbti FROM Users WHERE id=(%s)", (user_id,))
        user_mbti_tuple = self.cur.fetchall()

        companions = list()
        if not user_mbti_tuple:
            print(f"Usuário @{username} não cadastrado")
            response.append(f"@{username}, defina sua personalidade  MBTI antes com o comando mbti.")
            return companions

        mtbi_type = list(user_mbti_tuple[0])[0]

        self.cur.execute("SELECT username FROM Users WHERE mbti=(%s)", (POSSIBLE_COUPLES[mtbi_type],))
        matches = self.cur.fetchall()

        for user in matches:
            formated_companions = ''.join(map(str,user[0]))
            companions.append(formated_companions)
        
        return companions

    def endConnection(self):
        self.conn.commit()
        self.conn.close()   

POSSIBLE_COUPLES = {"ESTJ": "ISFP", "ISFP":"ESTJ",
          "ISTJ": "ESFP", "ESFP":"ISTJ",
          "INFP": "ENFJ", "ENFJ":"INFP",
          "INTP": "ENTJ", "ENTJ": "INTP",
          "ESTP": "ISFJ", "ISFJ": "ESTP",
          "ENTP": "INFJ", "INFJ": "ENTP",
          "ESFJ": "ISTP", "ISTP": "ESFJ",
          "ENFP": "INTJ", "INTJ": "ENFP"}
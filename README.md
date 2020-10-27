# kibot
Bot de Telegram com funções completamente estúpidas. Você pode utilizar ele em grupos para entretenimento ^^

## Adicionando o kibot a um grupo
<details>
    <summary> Tutorial</summary>
Para adicionar o bot em um grupo de Telegram clique em *Adicionar Membro* e pesquise por @sorvebot:

![Adicionar Membro](https://i.imgur.com/mZxd9K1.png)

![Adicionar kibot](https://i.imgur.com/gXocwyF.png)

E pronto, agora você pode usar o bot!!!! Digite / no chat para ver os comandos possíveis e uma breve descrição de cada um deles. Para uma descrição mais detalhada do uso dos comandos, utilize /help.
</details>

## Criando o seu próprio kibot
Primeiro, clone o repositório na sua máquina e instale as dependências usando os comandos abaixo:
```
git clone https://github.com/kibonusp/kibot.git
cd kibot
pip install -r requirements.txt
```
Agora, para você administrar um kibot, primeiro crie um bot usando o comando /newbot do @BotFather. Após isso, pegue o token e crie um arquivo informacoes.py contendo o token dentro do diretório kibot/Libraries e o appname do Heroku, caso vá usar.

![informacoes.py](https://i.imgur.com/zwwjLuL.png)

E está pronto ^^
Para rodar o bot na sua máquina, simplesmente execute o comando
```
python3 mainLocal.py
```

## Hosteando o kibot no Heroku
Para hostear o kibot no Heroku, recomendo seguir [esse tutorial](https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2) e fazer as modificações necessárias para isso.
Vai ser necessário criar um banco de dados Postgres. Para isso, rode o seguinte código:
```
heroku addons:create heroku-postgresql:hobby-dev
```
Após isso, vá no seu servidor do Heroku, e pegue o Heroku CLI e copie no repertório. Após isso, você terá que definir a tabela do seu banco de dados. Para isso, use:
```
CREATE TABLE User (
    id INTEGER UNIQUE.
    username TEXT,
    mbti TEXT
);
```
Para sair, use ```Ctrl + K```

## Comandos
Os comandos ~~inúteis~~ atuais do bot são esses:
| Comando | Descrição | Uso |
|---------|-----------|-----|
| /start  | Mensagem de início do bot | /start |
| /mbti   | Define a personalidade MBTI de um usuário | /mbti [MBTI]|
| /casais | Retorna parceiros possíveis dado o MBTI do usuário | /casais |
| /parceiro | Retorna um parceiro aleatório dado o MBTI do usuário | /parceiro |
| /furry | Retorna imagens de furry aleatórias | /furry |
| /dividegrupos | Divide pessoas em grupos aleatórios | /dividegrupos [Pessoa 1] [Pessoa 2] ... [Tamanho do Grupo]
| /audio | Envia um áudio engraçado aleatório | /audio |
| /ping | Envia um áudio com ping | /ping |
| /pong | Envia um áudio com pong | /pong |
| /cancelado | Cancela alguém | /cancelado [Pessoa] |
| /pingpong | Joga uma partida de ping-pong | /pingpong [Pessoa1] [Pessoa2] |
| /webcafune | Dá cafuné em alguém | /webcafune [Pessoa] |
| /webabraco | Dá um abraço em alguém | /webabraco [Pessoa] |
| /webbeijo | Dá um beijo em alguém | /webbeijo [Pessoa] |
| /dente | Retorna imagens de Odontologia | /dente |
| /kibon | Retorna deliciosos picolés Kibon | /kibon |
| /traduz | Converte um áudio em mensagem | /traduz *mande esse comando respondendo um áudio* |
| /help | Demonstra o uso de cada um dos comandos | /help |
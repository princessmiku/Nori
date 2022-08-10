from etc.bot.botClient import client

import slash

if __name__ == '__main__':
    __token = open('config/token.txt').read()
    client.run(__token)

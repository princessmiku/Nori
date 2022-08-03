from etc.bot.botClient import client

if __name__ == '__main__':
    client.run(open('config/token.txt').read())

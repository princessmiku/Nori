import sys

from etc.banned_words import check_BadWord

print(check_BadWord("hey du arschloch"))
sys.exit()
from etc.bot.botClient import client
from etc import search
import slash
if __name__ == '__main__':
    __token = open('config/token.txt').read()
    client.run(__token)


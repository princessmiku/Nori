from configparser import ConfigParser

from .checkExists import CheckExists


class GenerateStructure:


    def __init__(self, checkExists: CheckExists):
        self.checkExists = checkExists
        self.finish: bool = False

        self.gs_config()
        self.gs_output()

    def gs_config(self):
        self.checkExists.checkFolderAndCreate("./config")
        self.checkExists.checkFileAndCreate("./config/token.txt", "ENTER YOUR TOKEN THERE")
        self.checkExists.checkFileAndCreate("./config/.gitignore", "*")
        notExists: bool = self.checkExists.checkFileAndCreate("./config/bot.ini")
        if notExists:
            config = ConfigParser(); config.read(self.checkExists.getValidPath("./config/bot.ini"))
            config.add_section("DISCORD")
            config.add_section("URL")
            config.set("DISCORD", "bot_owner", "ID HERE")
            config.set("DISCORD", "bot_status", "Play with someone")
            config.set("DISCORD", "bot_guild", "ENTER YOUR BOT GUILD HERE")
            config.set("URL", "bot_invite", "SET A CUSTOM INVITE")
            config.set("URL", "github_repo", "SET A LINK TO THE GITHUB REPO")
            config.set("URL", "vote", "SET A LINK FOR VOTING")
            config.write(open(self.checkExists.getValidPath("./config/bot.ini"), mode='w'))

    def gs_output(self):
        self.checkExists.checkFolderAndCreate("./output")
        self.checkExists.checkFileAndCreate("./output/.gitignore", "*")

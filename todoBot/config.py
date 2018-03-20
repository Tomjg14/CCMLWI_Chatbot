class Config:

    def __init__(self):
        self.TOKEN = ""
        self.OWMKEY = ""
        with open("config_info.txt") as infile:
            self.TOKEN = infile[0][:-1]
            self.OWMKEY = infile[1]
        self.URL = "https://api.telegram.org/bot{}/".format(self.TOKEN)

    def getToken(self):
        return self.TOKEN

    def getOWMKEY(self):
        return self.OWMKEY

    def getURL(self):
        return self.URL
    

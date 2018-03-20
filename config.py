class Config:

    def __init__(self):
        self.TOKEN = ""
        with open("config_info.txt") as infile:
            for line in infile:
                self.TOKEN = line
        self.URL = "https://api.telegram.org/bot{}/".format(self.TOKEN)

    def getToken(self):
        return self.TOKEN

    def getURL(self):
        return self.URL
    

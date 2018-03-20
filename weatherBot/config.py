class Config:

    def __init__(self):
        self.TOKEN = ""
        self.OWMKEY = ""
        with open("token.txt") as infile:
            for line in infile:
                self.TOKEN = line
        with open("owmkey.txt") as infile:
            for line in infile:
                self.OWMKEY = line
        self.URL = "https://api.telegram.org/bot{}/".format(self.TOKEN)

    def getToken(self):
        return self.TOKEN

    def getOWMKEY(self):
        return self.OWMKEY

    def getURL(self):
        return self.URL
    

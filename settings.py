class _SETTING():
    def __init__(self):
        self.settingBody = __import__("codecs").open("settings.json","r",encoding="UTF-8").read()
        self.lookupIDS = __import__("json").loads(self.settingBody)['IDS']
        self.textArr = __import__("json").loads(__import__("codecs").open("placeHolder.json","r",encoding="UTF-8").read())
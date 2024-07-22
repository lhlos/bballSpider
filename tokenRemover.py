import re

def removeToken(text):
    cleanText = str(text).replace("[","").replace("]","").replace("'","").replace('"',"").replace("{","").replace("}","")
    return cleanText

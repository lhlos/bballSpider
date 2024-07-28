def removeToken(text):
    cleanText = str(text).replace("[","").replace("]","").replace("'","").replace('"',"").replace("{","").replace("}","")
    return cleanText

def replaceDash(text):
    cleanText = text.replace("-","-1")
    return cleanText
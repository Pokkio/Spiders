from fontTools.ttLib import TTFont

font = TTFont('./font/2.ttf')
font.saveXML('2.xml')

# Python Script, API Version = V15

import re
import sys

def rename_part(currentPart):
    i=0;
    for subpart in currentPart.Components:
        my_template = subpart.Template
        properties = my_template.CustomProperties
        
        
        if not properties.ContainsKey("BENENNUNG"):
            rename_part(my_template)
            
        try:
            benennung = properties["BENENNUNG"]
            
            benennung_value = benennung.Value
            #print type(benennung_value)
            #benennung_value = 
            
            
            my_template.Name = benennung_value;
            # ^ Anfang des Strings
            # []: alle Zeigen in Klammer werden gematcht, nicht noetig hier, aber besser lesbar
            # * letzter ausdruck beliegind oft (0-unendlich)
            #my_template.Name=re.sub("^Bauraummodell[ ]*","",my_template.Name)
            
            # ?<=: Vorbedingung
            # Ab Zeichen xx werden yy Zeichen gelöscht
            #my_template.Name=re.sub("(?<=^.{xx}).yy}","",my_template.Name)
            # Ab Zeichen xx werden bis zu yy Zeichen gelöscht
            #my_template.Name=re.sub("(?<=^.{xx}).{0,yy}","",my_template.Name)
            
            
            # $ steh fuer das ende
            # \d: eine Ziffer
            #my_template.Name=re.sub("_M\d+$","",my_template.Name)
            
            # \g<0> : gesamtehr match
            # \g<1>.... \g<?>: Nte klammerung / gruppe
            #my_template.Name=re.sub("(_M\d+$)"," Hallo \g<1>",my_template.Name)
            
            my_template.Name=re.sub("(.*)_(M\d+$)","\g<2> - \g<1>",my_template.Name)
            
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print my_template.Name
            print benennung_value
            continue

part = GetRootPart()
rename_part(part)

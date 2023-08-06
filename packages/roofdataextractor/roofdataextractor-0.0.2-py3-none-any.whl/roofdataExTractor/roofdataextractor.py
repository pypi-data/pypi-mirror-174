### Version 1.0

# Python 3 only

# Defused xml prachekina daug attacku, kurios gali but xml'e, tai pasiskaitysim ka tiksliai kai baigsim

from xmljson import badgerfish as bf
from defusedxml.ElementTree import fromstring
import defusedxml.ElementTree as ET
import json


def check_format(file):
    try:
        ET.parse(file)
        return True
    except ET.ParseError:
        # if the file is not well-formed, print that is not well-formed
        print(file + " is not well-formed")
        return False



# define a function to convert xml to json
def xml_to_json(file):

 if file.endswith(".xml"):
    # if the file is well-formed...
    if check_format(file):
        # get file name   
        name = str.split(file, ".")[-2]
        # open the XML file, convert to json and dump into a new file
        with open(file, "r") as input:
            jsonOut = bf.data(fromstring(input.read()))
            with open(name + ".json","w+") as newFile:
                json.dump(jsonOut, newFile, ensure_ascii=False)


def main():
    file=input("Iveskite failo pavadinima arba kelia iki jo: ")
    xml_to_json(file)

if __name__ == '__main__':
    main()
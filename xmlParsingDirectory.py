import xml.etree.ElementTree as ET
from xml.etree.ElementTree import *
import os
import pandas as pd
from xml.dom.minidom import parse
from collections import Counter
import csv


path='D:\\inputfiles'

finaldata=[]
for filename in os.listdir(path):
    final_output = {}
    if not filename.endswith('.xml'):continue
    fullname=os.path.join(path,filename)
    tree = ET.parse(fullname)
    userAgents = tree.getroot()
    print filename

    def printTags(userAdress, tagList, inputList):
        if (len(userAdress) > 0):
            tagList = tagList + str(userAdress.tag) + "-"
            for userAdressChild in userAdress:
                if (len(userAdressChild) > 0):
                    printTags(userAdressChild, tagList, inputList)
                else:
                    a = str(tagList) + str(userAdressChild.tag)
                    inputList.append(a)
        # print inputList
        return inputList
    for userAdress in userAgents:

        # inputList.append(userAdress.tag)
        inputList = []
        tagList = ""
        output = printTags(userAdress, tagList, inputList)
        counts = Counter(output)
        # print counts
        for s, num in counts.items():
            if num > 1:  # ignore strings that only appear once
                if num>4:
                    for suffix in range(0, 4):  # suffix starts at 1 and increases by 1 each time
                        output[output.index(s)] = s + "-" + str(suffix)  # replace each appearance of s
                else:
                    for suffix in range(0, num):  # suffix starts at 1 and increases by 1 each time
                        output[output.index(s)] = s + "-" + str(suffix)  # replace each appearance of s
            elif num ==1:
                output[output.index(s)] =s+"-"+str(0)
        # print output
        for i in output:
            a = str(i).split("-")
            c = ""
            if (a[-1]=="0"):
                for b in a[:-1]:
                    c = c + b + "/"
                c = c[:-1]
                # print i, c
                final_output[i[:-2]] = tree.find(c).text
            elif(not a[-1].isdigit()):
                print ""
            else:
                for b in a[:-1]:
                    c = c + b + "/"

                c = c[:-1]
                final_output[i] = tree.findall(c)[int(a[-1])].text
                # print i, tree.findall(c)[int(a[-1])].text

    # print final_output
    finaldata.append(final_output)

data=pd.DataFrame(finaldata)

print data

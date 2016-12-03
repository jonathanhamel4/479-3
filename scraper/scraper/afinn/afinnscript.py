from afinn import Afinn
import sys
import os
import json

def getAfinnScore(text_string, dept_id):
    afinn = Afinn()
    scored_doc = afinn.score(text_string)
    loadAfinnDict(scored_doc, str(dept_id))


def loadAfinnDict(score, dept):
    dirName = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(dirName, 'scores/afinnscores.json')
    #print filePath
    with open(filePath, 'r') as data_file:
        data = json.load(data_file)
        print dept
        scoreDoc = data.get(dept, 0)
        data[dept] = scoreDoc + score
        with open(filePath, 'w') as data_file2:
            json.dump(data, data_file2)

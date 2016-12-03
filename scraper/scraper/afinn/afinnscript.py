from afinn import Afinn
import sys
import os
import json

def getAfinnScore(text_string, dept_id):
    afinn = Afinn()
    scored_doc = afinn.score(text_string)
    #print scored_doc
    loadAfinnDict(scored_doc, str(dept_id))


def loadAfinnDict(score, dept):
    dirName = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(dirName, 'scores/afinnscores.json')
    #print filePath
    with open(filePath, 'r') as data_file:
        data = json.load(data_file)
        print dept
        scoreJson = data.get(dept, {})
        scoreDoc = scoreJson.get("score", 0)
        numberDoc = scoreJson.get("docs", 0)
        scoreJson["score"] = scoreDoc + score
        scoreJson["docs"] = numberDoc + 1
        data[dept] = scoreJson
        with open(filePath, 'w') as data_file2:
            json.dump(data, data_file2)

from afinn import Afinn

def getAfinnScore(text_string):
    afinn = Afinn()
    scored_sentences = afinn.score(text_string)
    print str(scored_sentences)

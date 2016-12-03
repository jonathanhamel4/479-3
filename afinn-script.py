from afinn import Afinn

def getScore(text_array):
    afinn = Afinn()
    scored_sentences = (afinn.score(text) for text in text_array)
    print str(scored_sentences)

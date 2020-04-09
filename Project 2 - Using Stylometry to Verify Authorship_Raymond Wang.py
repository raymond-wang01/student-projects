# CITS1401 PROJECT 2 - USING STYLOMETRY TO VERIFY AUTHORSHIP
    # By Raymond Wang 2019
    # A program to analyze the similarity of two pieces of text

##########################################

import os
import math


### PART 1 - INPUT ###
def main(textfile1 = None, textfile2 = None, feature = None, *args):
    # Check if input is missing arguments
    if textfile1 == None or textfile2 == None or feature == None:
        return("Input is missing arguments")
    
    #Check if input is a valid feature
    featureList = ['conjunctions', 'unigrams', 'punctuation', 'composite']
    if not feature in featureList:
        return(feature, 'is not a valid feature')
    
    #Check if file exists, then checks if file can be decoded
    if not os.path.isfile(textfile1):
        return(textfile1, 'could not be found')
    else:
        try:
            text1 = open(textfile1, "r").read()
        except UnicodeDecodeError:
            return(textfile1, 'could not be decoded')     
    if not os.path.isfile(textfile2):
        return(textfile2, 'could not be found.')
    else:
        try:
            text2 = open(textfile2, "r").read()
        except UnicodeDecodeError:
            return(textfile2, 'could not be decoded')
    
    #Check if input has too many arguments
    try:
        dist, prof1, prof2 = main_(text1, text2, feature, *args)
        return(dist, prof1, prof2)    
    except (ValueError, TypeError):
        return("There are too many arguments in input")


def main_(text1, text2, feature):
    
    if feature == 'conjunctions':
        conjunc1 = conjunctions(text1)
        conjunc2 = conjunctions(text2)
        dist = distance(conjunc1, conjunc2)
        return(dist, conjunc1, conjunc2)
        
    elif feature == 'unigrams':
        unigrams1 = unigrams(text1)
        unigrams2 = unigrams(text2)
        dist = distance_unigrams(unigrams1, unigrams2)
        return(dist, unigrams1, unigrams2)
        
    elif feature == 'punctuation':
        punc1 = punctuation(text1)
        punc2 = punctuation(text2)
        dist = distance(punc1, punc2)
        return(dist, punc1, punc2)
         
    elif feature == 'composite':
        comp1 = composite(text1)
        comp2 = composite(text2)
        dist = distance(comp1, comp2)
        return(dist, comp1, comp2)
    
    else:
        return
   
   
### PART 2 - FEATURES ###
    
#########################################
## CONJUNCTIONS FEATURE
def conjunctions(text):
    punc = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~'
    for char in punc:
        text = text.replace(char, ' ')
    
    #Removes '--', makes text lowercase and splits text
    tNoPunc = text.replace('--', ' ')
    textLower = tNoPunc.lower()
    textList = textLower.split()
    
    #Creates dictionary with required conjunctions
    conjuncList = ["also", "although", "and", "as", "because", "before", "but", "for", "if", "nor", "of",
                   "or", "since", "that", "though", "until", "when", "whenever", "whereas",
                   "which", "while", "yet"]
    conjunc = dict((i,0) for i in conjuncList)
    
    #Counts words if they are in conjuncList
    for word in textList:
        if word in conjuncList:
            conjunc[word] = conjunc.get(word, 0) + 1
    
    return(conjunc)


#########################################
## UNIGRAMS FEATURE
def unigrams(text):
    punc = '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~”“‘'
    for char in punc:
        text = text.replace(char, ' ')
    
    text = text.replace('--', ' ')
    textLower = text.lower()
    textList = textLower.split()
    
    unigramsdict = {}
    for word in textList:
        unigramsdict[word] = unigramsdict.get(word, 0) + 1
    while("'" in unigramsdict):
        unigramsdict.pop("'")
    while('' in unigramsdict):
        unigramsdict.pop('')
    while('–' in unigramsdict):
        unigramsdict.pop('–')
    while('-' in unigramsdict):
        unigramsdict.pop('-')
    while('’' in unigramsdict):
        unigramsdict.pop('’')
    
    return(unigramsdict)


#########################################
## PUNCTUATION FEATURE
def punctuation(text):
    punc = '!"#$%&()*+./:<=>?@[\\]^_`{|}~'
    for char in punc:
        text = text.replace(char, ' ')
    tNoPunc = text.replace('--', ' ')
    textList = tNoPunc.split()
    
    puncList = [',', ';', '-', "'"]
    punc = dict((i,0) for i in puncList)
       
    for word in textList:
        for p in [',', ';']:
            punc[p] += word.count(p)
        if word.count("-") > 0:
            puncSearch("-", word, punc)
        if word.count("'") > 0:
            puncSearch("'", word, punc)
    
    return(punc)

# Counts hyphens surrounded by words
def puncSearch(char, word, puncDict):
    puncCount = word.count(char)
    if puncCount == 1:
        puncIndex = word.find(char)
        indexBefore = puncIndex - 1
        indexAfter = puncIndex + 1
        if indexBefore >= 0 and word[indexBefore].isalpha() and indexAfter <= len(word) - 1 and word[indexAfter].isalpha():
            puncDict[char] += 1
    elif puncCount > 1:
        multiPuncInd = list(findAll(word, char))
        multiIndBefore = [x - 1 for x in multiPuncInd]
        multiIndAfter = [x + 1 for x in multiPuncInd]
        for i, j in zip(multiIndBefore, multiIndAfter):
            if i >= 0 and word[i].isalpha() and j <= len(word) - 1 and word[j].isalpha():
                puncDict[char] += 1
            

# Finds index of all punctuation in words which may have more than one hyphens or single quotes
def findAll(word, char):
    startInd = 0
    while True:
        startInd = word.find(char, startInd)
        if startInd == -1: return
        yield startInd
        startInd += len(char)


#########################################
## COMPOSITE FEATURE
def composite(text):
    conjunc = conjunctions(text)
    punc = punctuation(text)
    #unigramsdict = unigrams(text)
    
    #numWords = sum(unigramsdict.values())
    
    comp = {**conjunc, **punc}
    
    text = text.replace('--', ' ')
    
    wordList = text.split()
    # Returns sequence of words as well as splitting floating point numbers into two words e.g. 12.45 -> 12, 45
    wordList = wordSequence(wordList)
    # Finds numberof words from sequence
    numWords = len(wordList)
    
    # Indicates end of sentences with '@@' so that text can be split by sentences
    sentenceString = ' '.join(str(word) for word in wordList)
    sentenceReplaced = sentenceString.replace('. ', '@@')
    sentenceReplaced = sentenceReplaced.replace('."', '@@')
    sentenceReplaced = sentenceReplaced.replace('!"', '@@')
    sentenceReplaced = sentenceReplaced.replace('! ', '@@')
    sentenceReplaced = sentenceReplaced.replace('?"', '@@')
    sentenceReplaced = sentenceReplaced.replace('? ', '@@')
    
    # Splits text into sentences and finds number of sentences from sequence
    sentenceList = sentenceReplaced.split('@@')
    numSentences = len(sentenceList)
    avgWords = round(numWords / numSentences, 4)
    
    #Splits paragraphs and finds number of paragraphs from sequence
    paragraphList = text.split('\n\n')
    numParagraphs = len(paragraphList)
    avgSentences = round(numSentences / numParagraphs, 4)
    
    comp['words_per_sentence'] = avgWords
    comp['sentences_per_par'] = avgSentences
    
    return(comp)


## Returns sequence of words as well as splitting floating point numbers into two words e.g. 12.45 -> 12, 45
def wordSequence(wordList):
    w = []
    for word in wordList:
        index = word.find('.')
        indexBefore = index - 1
        indexAfter = index + 1
        if indexBefore >= 0 and word[indexBefore].isdigit() and indexAfter <= len(word) - 1 and word[indexAfter].isdigit():
            #word = word[:index] + ' ' + word[index + 1:]
            w.append(word[:index])
            w.append(word[index+1:])
        else:
            w.append(word)
    return(w)


### PART 3 - OUTPUT ###

#########################################
## FINDING DISTANCE

def distance(p1, p2):
    distanceDict = {key: (p1[key] - p2[key])**2 for key in p1.keys()}
    dist = round(math.sqrt(sum(distanceDict.values())), 4)
    return(dist)

def distance_unigrams(p1, p2):
    #Creates dictionaries with all keys in both p1 and p2
    combined = {**p1, **p2}
    
    #Finds distance using combined keys. Thus, if key is in p2 and not in p1, it returns value of 0 for p1 and vice versa
    distanceDict = {key: (p1.get(key,0) - p2.get(key,0))**2 for key in combined.keys()}
    dist = round(math.sqrt(sum(distanceDict.values())), 4)
    
    return(dist)






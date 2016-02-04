#!/usr/bin/env python
# -*- coding:utf-8 -*-

def findWordInLines(word,linesCopy):
    finded = []
    i = 0
    index = []
    for line in linesCopy:
        start = line.index('{')
        end =  line.index('}')
        wordsLine = line[(start+1):end]
        wordsLine = wordsLine.split(',')

        for w in wordsLine:
            if w.strip() == word.strip():
                finded.append(line)
                index.append(i)
                i = i+1
                break
        i = i+1

    i = len(index)
    
    while i > 0:
        linesCopy.pop(i-1)
        i = i - 1
    
    return linesCopy,finded

def main():
    f = open('/home/panceri/git/alpes_v1/base_tep2/base_tep.txt', 'r')
    novaWordNet = open('/home/panceri/git/alpes_v1/base_tep2/novaWordNet.txt', 'w')

    lines = f.readlines()

    line = lines[0]
    print "inicio"
    print (line)
     

    start = line.index('{')
    end =  line.index('}')


    words = line[(start+1):end]
    words = words.split(',')
    lines.pop(0)
#     print len(lines)
    i=0
    lenwords = len(words)
    while i < lenwords:
        word = words[i]
        rtn  = findWordInLines(word,lines)
        lines = rtn[0]

        wordsAppend = []
        
        for findedLine in rtn[1] :
            start = findedLine.index('{')
            end =  findedLine.index('}')
            for w in findedLine[(start+1):end].split(','):
                wordsAppend.append(w)
        
        for w in wordsAppend:
            valid = True
            for e in words:
                if e.strip() == w.strip():
                    valid = False
                    
            if valid:
                words.append(w+" ")
        
        
        
        lenwords = len(words)
        
#         print ("{2} - {0} - {1}".format(i,len(words),len(lines)))
        i = i + 1
#     print words
    num = 1
    auxWords = num.__str__()+"."+" "+"{"+words.__str__()+"}"
    num = num + 1
    print auxWords
    novaWordNet.writelines(auxWords)
    novaWordNet.close()
    print len(lines)
    print len(words)
    print "fim"
#     exit()


if __name__ == "__main__":
    main()
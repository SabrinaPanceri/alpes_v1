# -*- coding: utf-8 -*-
#encoding =utf8
import codecs
# import re

def organizaWordNet(word,linesCopy):
    finded = []
    i = 0
    for line in linesCopy:
        start = line.index('{')
        end =  line.index('}')
        wordsLine = line[(start+1):end]
        wordsLine = wordsLine.split(',')

        for w in wordsLine:

            if w.strip() == word.strip():
                
                finded.append(line)
                linesCopy.pop(i)
                i = i+1
                break
        i = i+1
    return linesCopy,finded


#PARA EXECUTAR O ARQUIVO .py SEM PRECISAR INTEGRAR COM O DJANGO!!!!
def main():
    f = codecs.open('/home/panceri/git/alpes_v1/base_tep2/base_tep.txt', 'r', 'UTF8')

    lines = f.readlines()

    line = lines[0]

    print (line)

    start = line.index('{')
    end =  line.index('}')
    aux = []

    words = line[(start+1):end]
    words = words.split(',')
#     lines.pop(0)
    aux.append()
    
    print len(lines)
    i=0
    lenwords = len(words)
    while i < lenwords:
        word = words[i]
        rtn  = organizaWordNet(word,lines)
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
                words.append(w)
        
        lenwords = len(words)
        
        print ("{2} - {0} - {1}".format(i,len(words),len(lines)))
        i = i + 1

    print len(lines)
    exit()

#PARA EXECUTAR O ARQUIVO .py SEM PRECISAR INTEGRAR COM O DJANGO!!!!
if __name__ == "__main__":
    main()




















# 
# def organizaWordnet():
# 
#     base_tep = codecs.open('/home/panceri/git/alpes_v1/base_tep2/base_tep.txt', 'r', 'UTF8')
#     wordnet = []
#     #variavel com conteúdo do arquivo em memoria
#     #não imprimir essa variável, MUITO GRANDEE!!!
#     wordNet = base_tep.readlines()
#     
#     #fechar arquivo 
#     base_tep.close()
#     
# 
# ### 263. [Verbo] {consentir, deixar, permitir} <973>
# ### 1ª linha do arquivo
# ### 1. [Verbo] {exagerar, exceder, quinta-essenciar, rebuscar, refinar, requintar} 
#     
#     x = 0
#     for i in range(len(wordNet)):
#         print i
#         print "split", wordNet[i].split(" ")
#         
# #         print "termos",re.findall('{[^}]*}', i)
# #         
# #         print "num",re.findall('[[0-9]^.]*.', i)
#         exit()
#     
#     
#     
#     
#     
# #     for sinonimos in wordNet:
# #         print re.findall('{[^}]*}', sinonimos)
# #         exit()
#   
#     
#     
#     return True


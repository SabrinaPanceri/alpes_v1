#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re

def main():
    print "ARQUIVO PARA TESTE EM PYTHON PURO!"
    print 

    dicSin = {}
    dicSin['velocidade'] = [['18751', "apressuramento, celeridade, ligeireza, \
    pressa, rapidez, velocidade"]]
    dicSin['inovadores'] = [['7875', "inovador, inovante, novador"]]
    dicSin['tempo'] = [['1234', "tempo"]]
    dicSin['rapidez'] = [['18751', "apressuramento, celeridade, ligeireza, \
    pressa, rapidez , velocidade"]]
    
    
    texto = []
    
    texto.append("(velocidade, N), (informação, N), (tempos, N), (atuais, ADJ),\
     (mudo, V), (mundo, N), (negócios, N),\
     (negócios, N), (inovadores, ADJ), (respectivos, ADJ), \
     (concorrentes, N), (surgem, V), (forma, N), (rápida, ADJ), \
     (necessário, ADJ), (preparação, N), (planejamento, N), \
     (deve, V), (ser, V), (ágil, ADJ), (flexível, ADJ), \
     (fácil, ADJ), (ser, V), (adaptado, PCP), (necessário, ADJ),\
      (prover, V), (vantagem, N), (necessária, ADJ),\
      (opções, N), (aparecem, V), (mercado, N), (consumidor, N),\
       (torna, V), (exigente, ADJ), (requerendo, V), \
      (plano, N), (negócios, N), (preveja, V), \
      (formas, N), (desenvolver, V), (produto, N), (melhor, ADJ), \
      (qualidade, N), (maior, ADJ), (agilidade, N), (possível, ADJ), (rapidez, ADJ)")
    
    
#     print texto
#     print dicSin
    
#trabalhando com lista
    for sliceTexto in texto:
        auxkey = dicSin.keys()
        for aux in auxkey:
            if aux in sliceTexto:
                for text in sliceTexto.split():
                    text = text.replace("(","").replace(",","").replace(")","")
                    if aux in text:
                        print aux, text
                        
                        
                        
                        
                        
                        
        
        
        
        
        
#         if sliceTexto in dicSin.keys():
#             print sliceTexto, dicSin.keys()
    
    
#     for term, refTerm in dicSin.iteritems():
#         for texto1 in texto.split():
#             print texto1,term
#             if texto1 == term:
#                 for i in range(len(refTerm)):
#                     print i
#                 exit()
#             else:
#                 print "else", texto1


if __name__ == "__main__":
    main()
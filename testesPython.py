#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re



def main():
    
    st_tagcomAce_posInicial = [[(u'corret',u'V'), (u'signific',u'V'), (u'atend',u'V'), (u'dar',u'V'), (u'consider',u'V')] , \
                               [(u'atribu',u'V'), (u'atend',u'V'), (u'dar',u'V'), (u'consider',u'V')], \
                               [(u'consider',u'V'), (u'deix',u'V') , (u'atribu',u'V'), (u'atend',u'V'), (u'dar',u'V'), (u'consider',u'V'), (u'sabrina',u'V')]]
    norm_posInicial = []
    
    dicionario={}
    
    dicionario['dar'] = [[u'dar', u'deix', u'produz'], [u'atribu', u'confer', u'dar', u'imp', u'p\xf4r'], [u'dar', u'pag'], [u'dar', u'destin', u'oferec'], [u'atin', u'dar'], [u'brot', u'dar', u'deit', u'exal', u'lan\xe7'], [u'dar', u'decret', u'ler', u'profer', u'public'], [u'dar', u'execut', u'exib'], [u'atribu', u'dar', u'deleg', u'invest'], [u'abast', u'bast', u'cheg', u'dar'], [u'bat', u'dar', u'desborcel', u'desborcin', u'esborcel', u'esborcin', u'esboten', u'esbrucin', u'golp'], [u'alvissar', u'dar', u'defront', u'depar', u'encar', u'encontr', u'top'], [u'abon', u'administr', u'confer', u'dar', u'distribu', u'ministr', u'oferec'], [u'dar', u'declar', u'declin', u'diz', u'emit', u'enunci', u'exterior', u'extern', u'indic', u'manifest', u'mencion', u'pronunci', u'ter'], [u'alborc', u'camb', u'cambi', u'comut', u'dar', u'escamb', u'mud', u'troc', u'vari'], [u'abr', u'dar', u'escancar', u'espampar', u'facult', u'franqu'], [u'afix', u'assinal', u'assin', u'dar', u'decret', u'demarc', u'design', u'determin', u'disp', u'dit', u'estabelec', u'fix', u'imp', u'indic', u'mand', u'orden', u'preceitu', u'prescrev', u'sinal'], [u'adjudic', u'arbitr', u'assin', u'atribu', u'conced', u'confer', u'credit', u'dar', u'dispens', u'imprim', u'larg', u'outorg', u'vot'], [u'badal', u'bat', u'bimbalh', u'dar', u'dobr', u'garr', u'resso', u'so', u'tintinabul', u'to', u'toc'], [u'confer', u'dar', u'dispens', u'emprest', u'fornec', u'ministr', u'prest', u'subministr'], [u'atin', u'dar', u'descobr', u'descortin', u'desencobr', u'encontr', u'not', u'perceb'], [u'dar', u'desat', u'desfech', u'desped', u'emit', u'larg', u'rutil', u'solt'], [u'consagr', u'dar', u'dedic', u'destin', u'devot', u'dic', u'prest', u'rend', u'sagr', u'tribut'], [u'dar', u'find', u'result', u'tornar-s'], [u'comet', u'comiss', u'confi', u'dar', u'deix', u'deleg', u'deput', u'encarg', u'encarreg', u'encomend', u'incumb', u'recomend'], [u'dar', u'derram', u'despend', u'largu', u'liberal', u'prodigal', u'prodig'], [u'ced', u'dar', u'entreg', u'fornec', u'liber'], [u'dar', u'desagu', u'desemboc', u'morr', u'termin'], [u'anunci', u'comunic', u'cont', u'dar', u'inform', u'notici', u'notific', u'particip', u'relat', u'report'], [u'consagr', u'consign', u'dar', u'dedic', u'do', u'entreg', u'oferec', u'sacrific', u'vot'], [u'consider', u'dar', u'interpret', u'julg', u'olh', u'reput', u'sab', u'ter'], [u'cri', u'dar', u'engendr', u'faz', u'fornec', u'ger', u'par', u'produz', u'ter'], [u'amostr', u'dar', u'demonstr', u'denot', u'desembu\xe7', u'diz', u'express', u'inculc', u'indic', u'manifest', u'mostr', u'patent', u'paten', u'revel', u'rev', u'rev', u'testemunh', u'transverber'], [u'arrum', u'assent', u'casc', u'cavilh', u'dar', u'desfer', u'embut', u'encavilh', u'imping', u'lasc', u'pespeg', u'preg'], [u'concut', u'dar', u'encasquet', u'fal', u'imbu', u'imp', u'impregn', u'incut', u'induz', u'infiltr', u'infund', u'inspir', u'insufl', u'met', u'penhor', u'plant'], [u'aleg', u'alud', u'apont', u'cit', u'dar', u'mencion', u'pont', u'refer', u'report', u'toc'], [u'apresent', u'dar', u'estend', u'oferec', u'oferend', u'ofert', u'present', u'traz'], [u'apresent', u'dar', u'declar', u'enunci', u'explic', u'express', u'exprim', u'formul', u'inform', u'manifest', u'p\xf4r', u'present', u'signific'], [u'dar', u'produz', u'rend'], [u'aprego', u'assoalh', u'dar', u'derram', u'dessegred', u'difund', u'dilat', u'dissemin', u'divulg', u'espalh', u'expand', u'general', u'irradi', u'notici', u'pass', u'popular', u'precon', u'prego', u'proclam', u'profess', u'promulg', u'propag', u'propal', u'public', u'soalh', u'solh', u'sopr', u'universal', u'veicul', u'vulg', u'vulgar', u'zabumb'], [u'dar', u'ministr', u'oferec', u'prontific', u'serv']]
    dicionario['consider'] = [[u'consider', u'estim', u'prez'], [u'atend', u'consider', u'examin', u'observ'], [u'consider', u'pes', u'ponder', u'vers'], [u'conceb', u'congemin', u'consider', u'cuid', u'desconfi', u'imagin', u'julg', u'pens', u'sup'], [u'consider', u'suspe'], [u'afer', u'ajuiz', u'apreci', u'aquilat', u'avali', u'bitol', u'conhec', u'consider', u'discern', u'enxerg', u'examin', u'julg', u'med', u'ponder', u'quilat', u'sopes', u'tom', u'ver'], [u'arrazo', u'atent', u'cogit', u'conceb', u'consider', u'contempl', u'cuid', u'devan', u'discorr', u'discurs', u'especul', u'excog', u'imagin', u'mastig', u'matut', u'medit', u'pens', u'ponder', u'raciocin', u'razo', u'reflet', u'reflex', u'trabalh'], [u'acar', u'analis', u'consider', u'encar', u'mir'], [u'consider', u'dar', u'interpret', u'julg', u'olh', u'reput', u'sab', u'ter'], [u'consider', u'entend', u'hav', u'julg', u'opin']]
    dicionario['corret'] = [[u'acert', u'adequ', u'apropri', u'cert', u'corret'], [u'cert', u'corret', u'exat'], [u'air', u'capaz', u'corret', u'decent', u'decor', u'dign', u'direit', u'honest', u'honr', u'\xedntegr', u'prob', u'pundonor', u'ret', u's\xe9ri'], [u'casti\xe7', u'corret', u'pur', u'vernacul', u'vern\xe1cul'], [u'acert', u'consert', u'corret', u'corrig', u'emend', u'refeit', u'retific', u'revist'], [u'corret', u'incensur', u'irrepreens'], [u'cert', u'corret', u'v\xe1l']]
    dicionario['sabrina'] = []
    dicionario['signific'] = [[u'diz', u'signific'], [u'signific', u'traduzir-s'], [u'denot', u'design', u'emblem', u'figur', u'represent', u'signific', u'simbol', u'traduz'], [u'apresent', u'dar', u'declar', u'enunci', u'explic', u'express', u'exprim', u'formul', u'inform', u'manifest', u'p\xf4r', u'present', u'signific']]
    dicionario['menos'] = [[u'aind', u'ao', u'menos', u'pel', u'menos'], [u'aind', u'ao', u'menos', u'pel', u'menos'], [u'menos'], [u'ao', u'menos', u'pel', u'menos', u'sequ'], [u'ao', u'menos', u'pel', u'menos', u'sequ'], [u'nem', u'ao', u'menos', u'nem', u'sequ', u'sequ']]
    dicionario['faz'] = [[u'execut', u'faz', u'perfaz'], [u'acab', u'avi', u'complet', u'execut', u'faz'], [u'convert', u'faz', u'torn'], [u'comet', u'faz', u'perpetr', u'pratic'], [u'fabric', u'faz', u'forj', u'form', u'manufatur', u'obr', u'produz'], [u'descrev', u'faz', u'perfaz', u'produz', u'tra\xe7'], [u'amodel', u'comp', u'delin', u'escrev', u'faz', u'model', u'tec', u'tra\xe7'], [u'al\xe7', u'arquitet', u'constru', u'edific', u'elev', u'ergu', u'erig', u'fabric', u'faz'], [u'configur', u'conform', u'faz', u'represent'], [u'estabelecer-s', u'faz', u'rein'], [u'faz', u'trabalh'], [u'equival', u'eq\xfcival', u'faz', u'import', u'som', u'val'], [u'arranh', u'faz', u'ganh', u'lucr', u'obt', u'retir', u'utiliz'], [u'faz', u'transform'], [u'empreend', u'faz', u'interprend', u'interpres', u'realiz'], [u'cri', u'dar', u'engendr', u'faz', u'fornec', u'ger', u'par', u'produz', u'ter'], [u'afet', u'amostr', u'aparent', u'banc', u'disfar\xe7', u'dissimul', u'encen', u'faz', u'fing', u'parent', u'pos', u'simul'], [u'desdobrar-s', u'diligenci', u'empenhar-s', u'empenhorar-s', u'esfor\xe7ar-s', u'faz', u'forcej', u'intent', u'pretend', u'procur', u'trabalh'], [u'consum', u'cumpr', u'desempenh', u'execut', u'exerc', u'experienci', u'experiment', u'faz', u'obr', u'oper', u'pratic', u'profess', u'promov', u'realiz', u'resgat'], [u'declam', u'diz', u'faz', u'pronunci', u'recit']]
    
    
    for chave, val in dicionario.iteritems():
        auxDic = []
        for iV in range(len(val)):
            for iVa in val[iV]:
                if iVa not in auxDic:
                    auxDic.append(iVa)
                
        dicionario[chave] = auxDic
        
    
    for idST in range(len(st_tagcomAce_posInicial)):
        listAux = []
        for tupla in st_tagcomAce_posInicial[idST]:
            termoStr = tupla[0]
            print 'termoStr -> ', termoStr
            
            
            if len(listAux) == 0:
                listAux.append(termoStr)
                
            
            else:
                for elemento in listAux:
                    add = False
                    
                    if termoStr not in dicionario[elemento]:
                        add = True
                    else:
                        add = False
                        print "else"
                        break
                        
                if add == True:        
                    listAux.append(termoStr)
                    
                     
                
        print listAux 
  
        norm_posInicial.append(listAux)
     
     
    print 'norm_posInicial',norm_posInicial
                                
                                
                                
if __name__ == "__main__":
    main()
    
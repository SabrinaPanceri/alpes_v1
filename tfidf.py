# -*- coding:utf-8 -*-

from math import log
import mysql.connector

def tf(word,doc):
    all_num=sum([doc[key] for key in doc])
    return float(doc[word])/all_num

def idf(word,doc_list):
    all_num=len(doc_list)
    word_count=0
    for doc in doc_list:
        if word in doc:
            word_count+=1
    return log(all_num/word_count)

def tfidf(word,doc,doc_list):
    score=tf(word,doc)*idf(word,doc_list)
    return score

if __name__=='__main__':
    #doc1={'あとで読む':28,'webサービス':16,'web':14,'機械学習':2,'python':1}
    #doc2={'あとで読む':21,'webサービス':11,'web':14,'起業':5}
    #doc3={'あとで読む':126,'webサービス':116,'web':74,'プログラミング':12,'アダルト':1}
    #doc4={'あとで読む':8,'webサービス':3,'社会':2,'政治':1,'日本':1}

    #doc_list=[doc1,doc2,doc3,doc4]
    #i=1
    #for doc in doc_list:
    #    print '-'*20
    #    print 'doc%d' % i
    #    for word in doc:
    #        print '"%s":%f' % (word,tfidf(word,doc,doc_list))
    #    i+=1


    con = mysql.connector.connect(user='root', password='123456',
                              host='127.0.0.1',
                              database='articles_base')
    try:
        cur = con.cursor()

        cur.execute("SELECT codigo,titulo,keyword FROM articles")

        doc_list = []
        for (codigo,titulo,keyword) in cur:
            if(keyword):
                
                keys = keyword.split(',')

                doc = {}

                weight = len(keys) * 10

                for k in keys:
                    doc[k.strip()] = weight
                    weight -= 10

                #print  str(codigo) + " : " + str(doc)
            
                doc_list.append(doc)


        print len(doc_list)

        i=1
        for doc in doc_list:
            print '-'*20
            print 'doc%d' % i
            for word in doc:
                print '"%s":%f' % (word,tfidf(word,doc,doc_list))
            i+=1
        


    except mysql.connector.Error as e:
        print "Error %d : %s" %  (e.errno,str(e.msg))

    finally:    
        if con:
            con.close()
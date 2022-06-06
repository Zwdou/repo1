"""extract tags from tags"""
import pandas as pd
import os
import jieba

import re
import jieba.analyse as analyse

import spacy
import nltk
import pycorrector
from pycorrector.proper_corrector import ProperCorrector

def keyword_tfidf(content,nkey):
    """textRank"""
    ##keywords = SnowNLP(content).keywords(nkey)
    ##keywords = analyse.textrank(content, topK=nkey, allowPOS=('n', 'v', 'vn'))
    """tfidf"""
    keywords_tfidf = analyse.extract_tags(str(content), topK = nkey, withWeight=True)
    keywords = []
    for item in keywords_tfidf:
        keywords.append(item[0])
    return keywords

def keyword_textrank(content,nkey):
    """textRank"""
    keywords = analyse.textrank(" ".join(content), topK=nkey, allowPOS=('n', 'v', 'vn'))
    return keywords

def fenci(datas):
    cut_words = jieba.cut(datas)
    return list(cut_words)

def correct(data):
    #m = ProperCorrector()
    #corr_pc,detail = m.proper_correct(data)
    corr_pc,detail = pycorrector.correct(data)
    return corr_pc
    
def textProcess(text):
    if not text or text == '':
        return ''
    try:
        r4 =  "\\【.*?】+|\\《.*?》+|\\#.*?#+|[.!/_,$&%^*()<>+""'?@|:;~{}#]+|[——！\\\，。=？、：“”‘’￥……（）《》【】]"
        result = re.sub(r4,'',text)
        return result
    except:
        return ''

def tag_file(text_path):
    head, tail = os.path.split(text_path)
    print("start processing " + tail)
    tail = tail.replace(".txt","")
    try:
        f = open(text_path, encoding="utf8")
        dat = f.read()
        dat = dat[:dat.rfind('\n')]
    except:
        return ''
    #corr_dat = correct(dat)
    pro_dat = textProcess(dat)
    print(pro_dat)
    res_tf = keyword_tfidf(pro_dat,nkey=15)
    cut_dat = fenci(pro_dat)
    res_tr = keyword_textrank(cut_dat,nkey=15)
    res_all = res_tf+res_tr
    print(res_all)
    res = list(set(res_all))
    #with open(os.path.join(save_path,tail,str('_tags.txt')),'a', encoding='utf-8') as f :
    #    f.write("tags:")
    #    f.write(str(res) + '\n')
    return res

if __name__ == '__main__':
    tag_file(text_path="./tmp/test1.txt")
    
from fuzzywuzzy import fuzz
from operator import itemgetter
import os
import re
import enchant


def similarsearch(WordList,dict_sentence,DocName,min_similarity=None):

    if min_similarity==None:
        min_similarity=50   
   
    N=6
    Max=(len(WordList))*len(WordList)-sum(range(0,len(WordList)))
    Mark=0
    N_tot=dict_sentence['N_tot']
    N_sentence=len(dict_sentence['sentence'])
    N_search=dict_sentence['N_search']
    search_sentence=dict_sentence['sentence'][0+N_tot-N_search:-1-N_tot+N_search]
    for index,word in enumerate(WordList):
            b=fuzz.token_set_ratio(word.lower(),search_sentence.lower())
            if b>70:
                Mark=Mark+(len(WordList)-index)*b/100
    MARK=round(Mark/Max*100,0)
    
    WordList_lowercase=[a.replace('.','').replace(',','').replace(';','').lower() for a in WordList]
    if MARK>min_similarity:
        doc_name=DocName.split('\\')[-1]
        refword=WordList[0]
        SentencesAsListOfWords = dict_sentence['sentence'].split(' ')
        BoldfaceListOfWords=[]
        cursor=0
        for word in SentencesAsListOfWords:
            
            for WordL in WordList_lowercase:
                if (cursor>0+N_tot-N_search and cursor<N_sentence-N_tot+N_search) and WordL in word.lower() and ([e for e in [',',':','.',';','-','’'] if e in word.lower().replace(WordL,'')] or word.lower().replace(WordL,'')=='') :
                    BoldfaceListOfWords.append((word,1)) 
                    break
            else:
                BoldfaceListOfWords.append((word,0)) 
            cursor=cursor+len(word)+1
        similarity=MARK
        FindDict={'doc_name':doc_name,
                  'refword':refword,
                  'BoldfaceListOfWords':BoldfaceListOfWords,
                  'similarity':similarity,}
    else:
        return None                   
    return FindDict
    
def findinalltext(WordList,Dir):
    new_List_total=[]
    if WordList:
        List_Dict_EachDoc=[]
        max_length_of_text=len(' '.join(WordList))+5
        for root, dirs, files in os.walk(Dir):
            for file in files:
                if file.endswith(".txt"):
                    DocPath=os.path.join(root, file) 
                    kTerm=WordList[0].lower()
                    f = open(DocPath, "r", encoding='utf8')
                    string=f.read()
                    string=string.replace('\n',' ')
                    string=string.replace('\t','').replace('\r','').replace('\f','').replace('\v','').replace('\a','').replace('\b','')
                    
                    N=150
                    List_sentences=[]
                    Results = re.finditer(kTerm,string.lower())

                    for result in Results:
                        span=result.span()
                        # search_sentence=string[span[0]-max_length_of_text:span[1]+max_length_of_text]
                        sentence=string[span[0]-N:span[1]+N]
                        sentence='...'+sentence+'...'
                        List_sentences.append({
                            'sentence':sentence,
                            'N_tot':N+3, # 3 is due to '...' at begining and end of sentence.
                            'N_search':max_length_of_text,
                            })

                    for dict_sentence in List_sentences:
                        DocName=DocPath.replace('.txt','')
                        Dict=similarsearch(WordList,dict_sentence,DocName,50)
                        if Dict is not None:
                            List_Dict_EachDoc.append(Dict)                         
        new_List_total=sorted(List_Dict_EachDoc, key=itemgetter('similarity'), reverse=True) 
    return new_List_total  
    
def Text2WordList(text):
    WordList=text.split()
    Dict={}
    if '*' in text:
        for word in WordList:
            if word.endswith('***'):
                Dict[word.replace('*','')]=4
            elif word.endswith('**'):   
                Dict[word.replace('*','')]=3
            elif word.endswith('*'):   
                Dict[word.replace('*','')]=2
            else:
                Dict[word.replace('*','')]=1
    

        # sorting words based on the importance assigned in above block
        WordList=[k for k, v in sorted(Dict.items(), key=lambda item: item[1], reverse=True)]  
    else:
        WordList=[]   
    return WordList   

def pdf2txt(pdf_path,text_path):
    txt_dir=f'{text_path}/TXT'
    print(txt_dir)
    if not os.path.isdir(txt_dir):
        os.makedirs(txt_dir)
    for root, dirs, files in os.walk(pdf_path):
        for file in files:
            if file.endswith(".pdf"):
                path=os.path.join(root, file)
                filename=file.replace('pdf','txt')
                cmd=f'pdftotext "{path}" "{text_path}/TXT/{filename}"'
                try:
                    os.system(cmd)
                except Exception as e:
                    print(e)

def remove_nonsense_line(text_path):
    txt_dir=f'{text_path}/TXT'
    d = enchant.Dict("en_US") 
    N=60
    for root, dirs, files in os.walk(txt_dir):
            for file in files:
                if file.endswith(".txt"):
                    DocPath=os.path.join(root, file) 
                    f = open(DocPath, "r")
                    Lines=f.readlines()

                    correctLines=[]
                    for line in Lines:
                        List=line.split()
                        if len(List)>5 :
                            if len(List)<N:
                                counter=0
                                for w in List:
                                    if d.check(w):
                                        counter=counter+1
                                if counter/len(List)>0.5:
                                    correctLines.append(line) 
                            else:
                                correctLines.append(line) 
                        
                        
                    file = open(DocPath, "w")
                    for line in correctLines:
                        file.write(line)
                    file.close() #This close() is important
                    print("text file has been modified!")            
    print('\n PDFs to TEXT has been completed successfully! \n')

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name+'.pdf' in files:
            return os.path.join(root, name)
 
            
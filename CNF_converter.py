import copy
sentence =   ["implies", ["and", ["implies", "A", "B"], "C"], "D"]
buf = copy.deepcopy(sentence)
print sentence
def traverse(o, tree_types=(list, tuple)):
    if isinstance(o, tree_types):
        if o[0] == "iff":
            o[0] = "and" 
            new = ["implies"]
            new.append(o[1])
            new.append(o[2])
            new1 = ["implies"]
            new1.append(o[2])
            new1.append(o[1])
            o[1] = new
            o[2] = new1

        elif o[0] == "implies":
            o[0] = "or"
            new = ["not"]
            new.append(o[1])
            o[1] = new
                     
        for value in o:
            for subvalue in traverse(value):
                yield subvalue
    else:
        yield o
        
        
for value in traverse(sentence):
    a = 10


def demorgan_and(sentence):
    global change
    if isinstance(sentence, list):
        if sentence[0] == "not":
            if isinstance(sentence[1], list):
                    if sentence[1][0] == "and":
                        new = sentence[1]
                        sentence.pop()
                        sentence[0] = "or"
                        change = 1
                        for item in new[1:]:
                            if isinstance(item, list) and item[0] == "not":
                                sentence.append(item[1])
                            else:
                                sentence.append(["not", item])
        
        for elem in sentence:
            demorgan_and(elem)
            
def demorgan_or(sentence):
    global change
    if isinstance(sentence, list):
        if sentence[0] == "not":
            if isinstance(sentence[1], list):
                    if sentence[1][0] == "or":
                        new = sentence[1]
                        sentence.pop()
                        sentence[0] = "and"
                        change = 1
                        for item in new[1:]:
                            if isinstance(item, list) and item[0] == "not":
                                sentence.append(item[1])
                            else:
                                sentence.append(["not", item])
        
        for elem in sentence:
            demorgan_or(elem)

def double_negation(sentence):
    global change
    if isinstance(sentence, list):
        if isinstance(sentence[1], list):
            if sentence[1][0] == "not":
                if isinstance(sentence[1][1], list):
                    if sentence[1][1][0] == "not":
                       change = 1
                       sentence[1] = sentence[1][1][1]
                
        for index, elem in enumerate(sentence):
            double_negation(elem)
    
    return sentence
                   
change = 1
while(change):
    change = 0
    demorgan_and(sentence)
    demorgan_or(sentence)

change = 1
while(change):
    change = 0
    sentence = double_negation(sentence)

if sentence[0] == "not" and isinstance(sentence[1], list):
    sentence = sentence[1][1]

def Distributivity(sentence):
    
    if isinstance(sentence, str):
        return sentence
    if isinstance(sentence, list):     
        if (len(sentence) > 2):
            S=[]
            count = 0
            if (sentence[0] == 'or'):
                i=1                        #put all the conjunction on the left
                j=1
                while j<(len(sentence)):
                    if isinstance(sentence[j], list): 
                        if sentence[j][0] == "and":
                            s = sentence[j]
                            sentence[j] = sentence[i]
                            sentence[i] = s
                            i = i + 1
                            count = count + 1       # count the number of conjunctions
                    j = j + 1
            if count > 0 :              # if there are  any conjunctions
        
                while(count > 1):      # apply Distributivity on the conjunctions
                    sentence1 = sentence[1]
                    sentence2 = sentence[2]
                    S = ["and"]
                    for s1 in sentence1[1:len(sentence1)]:
                        S.append(["or", s1, sentence2])
                    sentence[1] =  S
                    del(sentence[2])
                    Distributivity(sentence[1])
                    count = count - 1 
    

                i = len(sentence) - 1  #apply Distributivity on the result and the rest of Expressions
                while (i > 1):
                    sentence1 = sentence[1]
                    sentence2 = sentence[2]
                    S = ["and"]
            
                    for s1 in sentence1[1:len(sentence1)]:
                        S.append(["or", s1, sentence2])
                    sentence[1] =  S
                    del(sentence[2])
                    Distributivity(sentence[1])                    
                    i = i - 1
                sentence = S
            else:
                k = 1 
                while k<len(sentence):
                    sentence[k] = Distributivity(sentence[k])
                    k = k + 1
                    
    return sentence
    
    
def AssociativityAND(sentence):
    
    
    if isinstance(sentence, str):
        return sentence
        
    elif isinstance(sentence, list):
        if(sentence[0] == 'and'):
            i=1
            while (i < len(sentence)) :
                while( (isinstance(sentence[i], list)) and (sentence[i][0] == "and") ):
                    for S in sentence[i][1:len(sentence[i])] :
                        sentence.append(S)
                    del(sentence[i])
                i = i + 1
        else:
            j = 1 
            while (j < len(sentence)) :
                sentence[j] = AssociativityAND(sentence[j])
                j = j + 1
    return sentence
    
def AssociativityOR(sentence):
    
    
    if isinstance(sentence, str):
        return sentence
        
    elif isinstance(sentence, list):
        if(sentence[0] == 'or'):
            i=1
            while (i < len(sentence)) :
                while( (isinstance(sentence[i], list)) and (sentence[i][0] == "or") ):
                    for S in sentence[i][1:len(sentence[i])] :
                        sentence.append(S)
                    del(sentence[i])
                i = i + 1
        else:
            j = 1 
            while (j < len(sentence)) :
                sentence[j] = AssociativityOR(sentence[j])
                j = j + 1
    return sentence

def Factor(sentence):

    if isinstance(sentence,str):
        return sentence
    
    if sentence[0] == "not":       # case of 1 literal
        return sentence
        
    if sentence[0] == "or":        # case of 1 Clause
        i=1
        while i < len(sentence):
            j =  i + 1 
            if isinstance(sentence[i], str):    # case  of  symbol
                while  j < len(sentence):
                    if ( (isinstance(sentence[j],str)) and (sentence[j] == sentence[i]) ):
                        del(sentence[j])
                    else: 
                        j = j + 1
            elif isinstance(sentence[i], list):    # case of ["not", Symbol]
                while  (j < len(sentence) and isinstance(sentence[i], list)): 
                    if ( (isinstance(sentence[j],list)) and (sentence[j][1]==sentence[i][1]) ):
                        del(sentence[j])
                    else:
                        j = j + 1
            i = i + 1                    
        
    if sentence[0] == "and":
        i = 1 
        while i < len(sentence):            
            if (isinstance(sentence[i], list) and (len(sentence[i])> 0)):
                if sentence[i][0] == "or":
                    sentence[i] = Factor(sentence[i])                
            i = i + 1
        
        i = 1
        while i < len(sentence):
            j = i + 1 
            if isinstance(sentence[i], str):    # case  of  symbol
                while  j < len(sentence):
                    if ( (isinstance(sentence[j],str)) and (sentence[j] == sentence[i]) ):
                        del(sentence[j])
                    else: 
                        j = j + 1
            elif ((isinstance(sentence[i], list)) and (sentence[i][0] == "not")):    # case of ["not", Symbol]
                while  j < len[sentence]:
                    if ( (isinstance(sentence[j],list)) and ((sentence[j][0] == "not")) and (sentence[j][1]==sentence[i][1]) ):
                        del(sentence[j])
                    else:
                        j = j + 1
            elif ((isinstance(sentence[i], list)) and (sentence[i][0] == "or")):    # case of a disjunction
                while  j < len(sentence):
                    equal = 0
                    if ((isinstance(sentence[j], list)) and (sentence[j][0] == "or")):
                        if len(sentence[j]) == len(sentence[i]):
                            ii = 1
                            equal = 0
                            while(ii < len(sentence[i])):
                                jj = 1
                                while(jj< len(sentence[j])):
                                    if sentence[i][ii] == sentence[j][jj]:
                                        equal += 1    
                                    jj = jj + 1
                                ii = ii + 1
                    if equal == len(sentence[j]) - 1:
                        del(sentence[j])
                    else:
                        j = j + 1
            i = i + 1
                
                
        if len(sentence) == 2:
            sentence = sentence[1]
        elif len(sentence) == 1:
            sentence = []
            print "Empty Sentence"
    return sentence

def CNF(sentence):
    sentence = Distributivity(sentence) 
    sentence = AssociativityAND(sentence)
    sentence = AssociativityOR(sentence)
    sentence = Factor(sentence)

    return sentence
        
flag = False
if(buf[0]=='or'):
        flag =True

CNF(sentence)

if(flag):
    print(sentence[1])
else:
    print sentence
import copy
#sentence = [ "and", [ "or", "P", [ "not", "Q"]], [ "and", [ "not", "R"], "P"]]
#sentence =  ["and", ["or", "A", "B"], ["or", "A", "A"]]
#sentence = ["or", ["and", "A", "B"], ["and", "B", "A"]]
#sentence = ["or", "A", "A"]
#sentence = ["and", "A", "A"]
sentence = ["implies", ["and", ["not", "R"], "B"], "W"]
#sentence = ["not", ["implies", ["implies", ["or", "P", ["not", "Q"]], "R"], ["and", "P", "R"]]]
#sentence = ["or", ["not", ["implies", "P", "Q"]], ["implies", "R", "P"]]
#sentence = ["not", ["not", ["not", ["not", ["not", "P"]]]]]
#sentence = ["or", ["and", "A", "B"], ["and", "C", "D"]]
#sentence =  ["implies", ["and", ["implies", "A", "B"], "C"], "D"]
print sentence

def traverse(o, tree_types=(list, tuple)):
    if isinstance(o, tree_types):
        if o[0] == "iff":
            o[0] = "and" 
            new = ["implies"]
            new.append(o[1])
            new.append(o[2])
            new1 = ["implies"]
            new1.append(o[2])
            new1.append(o[1])
            o[1] = new
            o[2] = new1
            
        elif o[0] == "implies":
            o[0] = "or"
            new = ["not"]
            new.append(o[1])
            o[1] = new
                     
        for value in o:
            for subvalue in traverse(value):
                yield subvalue
    else:
        yield o
        
        
for value in traverse(sentence):
    a = 10
       

def demorgan_and(sentence):
    global change
    
    if isinstance(sentence, list):
        if sentence[0] == "not":
            if isinstance(sentence[1], list):
                    if sentence[1][0] == "and":
                        new = sentence[1]
                        sentence.pop()
                        sentence[0] = "or"
                        change = 1
                        for item in new[1:]:
                            if isinstance(item, list) and item[0] == "not":
                                sentence.append(item[1])
                            else:
                                sentence.append(["not", item])
        
        for elem in sentence:
            demorgan_and(elem)
            
def demorgan_or(sentence):
    global change
    if isinstance(sentence, list):
        if sentence[0] == "not":
            if isinstance(sentence[1], list):
                    if sentence[1][0] == "or":
                        new = sentence[1]
                        sentence.pop()
                        sentence[0] = "and"
                        change = 1
                        for item in new[1:]:
                            if isinstance(item, list) and item[0] == "not":
                                sentence.append(item[1])
                            else:
                                sentence.append(["not", item])
        
        for elem in sentence:
            demorgan_or(elem)

def double_negation(sentence):
    global change
    if isinstance(sentence, list):
        if isinstance(sentence[1], list):
            if sentence[1][0] == "not":
                if isinstance(sentence[1][1], list):
                    if sentence[1][1][0] == "not":
                       change = 1
                       sentence[1] = sentence[1][1][1]
                
        for index, elem in enumerate(sentence):
            double_negation(elem)
    
    return sentence
                   
change = 1
while(change):
    change = 0
    demorgan_and(sentence)
    demorgan_or(sentence)

change = 1
while(change):
    change = 0
    sentence = double_negation(sentence)

if sentence[0] == "not" and isinstance(sentence[1], list):
    sentence = sentence[1][1]

def Distributivity(sentence):
    
    if isinstance(sentence, str):
        return sentence
    if isinstance(sentence, list):     
        if (len(sentence) > 2):
            S=[]
            count = 0
            if (sentence[0] == 'or'):
                i=1                        #put all the conjunction on the left
                j=1
                while j<(len(sentence)):
                    if isinstance(sentence[j], list): 
                        if sentence[j][0] == "and":
                            s = sentence[j]
                            sentence[j] = sentence[i]
                            sentence[i] = s
                            i = i + 1
                            count = count + 1       # count the number of conjunctions
                    j = j + 1
            if count > 0 :              # if there are  any conjunctions
        
                while(count > 1):      # apply Distributivity on the conjunctions
                    sentence1 = sentence[1]
                    sentence2 = sentence[2]
                    S = ["and"]
                    for s1 in sentence1[1:len(sentence1)]:
                        S.append(["or", s1, sentence2])
                    sentence[1] =  S
                    del(sentence[2])
                    Distributivity(sentence[1])
                    count = count - 1 
    

                i = len(sentence) - 1  #apply Distributivity on the result and the rest of Expressions
                while (i > 1):
                    sentence1 = sentence[1]
                    sentence2 = sentence[2]
                    S = ["and"]
            
                    for s1 in sentence1[1:len(sentence1)]:
                        S.append(["or", s1, sentence2])
                    sentence[1] =  S
                    del(sentence[2])
                    Distributivity(sentence[1])                    
                    i = i - 1
                sentence = S
            else:
                k = 1 
                while k<len(sentence):
                    sentence[k] = Distributivity(sentence[k])
                    k = k + 1
                    
    return sentence
    
    
def AssociativityAND(sentence):
    
    
    if isinstance(sentence, str):
        return sentence
        
    elif isinstance(sentence, list):
        if(sentence[0] == 'and'):
            i=1
            while (i < len(sentence)) :
                while( (isinstance(sentence[i], list)) and (sentence[i][0] == "and") ):
                    for S in sentence[i][1:len(sentence[i])] :
                        sentence.append(S)
                    del(sentence[i])
                i = i + 1
        else:
            j = 1 
            while (j < len(sentence)) :
                sentence[j] = AssociativityAND(sentence[j])
                j = j + 1
    return sentence
    
def AssociativityOR(sentence):
    
    
    if isinstance(sentence, str):
        return sentence
        
    elif isinstance(sentence, list):
        if(sentence[0] == 'or'):
            i=1
            while (i < len(sentence)) :
                while( (isinstance(sentence[i], list)) and (sentence[i][0] == "or") ):
                    for S in sentence[i][1:len(sentence[i])] :
                        sentence.append(S)
                    del(sentence[i])
                i = i + 1
        else:
            j = 1 
            while (j < len(sentence)) :
                sentence[j] = AssociativityOR(sentence[j])
                j = j + 1
    return sentence

def Factor(sentence):
    if isinstance(sentence,str):
        return sentence
    
    if sentence[0] == "not":       # case of 1 literal
        return sentence
    if sentence[0] == "or" and (len(sentence)==3):
            if(sentence[1]==sentence[2]):
                sentence[0]=sentence[1]
                del(sentence[1])
            
                
    if sentence[0] == "or":        # case of 1 Clause
        i=1
        while i < len(sentence):
            j =  i + 1 
            if isinstance(sentence[i], str):    # case  of  symbol                        
                while  j < len(sentence):
                    if ( (isinstance(sentence[j],str)) and (sentence[j] == sentence[i]) ):
                        del(sentence[j])
                    else: 
                        j = j + 1
            elif isinstance(sentence[i], list):    # case of ["not", Symbol]
                while  (j < len(sentence) and isinstance(sentence[i], list)): 
                    if ( (isinstance(sentence[j],list)) and (sentence[j][1]==sentence[i][1]) ):
                        del(sentence[j])
                    else:
                        j = j + 1
            i = i + 1                    
        
    if sentence[0] == "and":
        i = 1 
        while i < len(sentence):            
            if (isinstance(sentence[i], list) and (len(sentence[i])> 0)):
                if sentence[i][0] == "or":
                    sentence[i] = Factor(sentence[i])                
            i = i + 1        
        i = 1
        while i < len(sentence):
            j = i + 1 
            if isinstance(sentence[i], str):    # case  of  symbol
                while  j < len(sentence):
                    if ( (isinstance(sentence[j],str)) and (sentence[j] == sentence[i]) ):
                        del(sentence[j])
                    else: 
                        j = j + 1
            elif ((isinstance(sentence[i], list)) and (sentence[i][0] == "not")):    # case of ["not", Symbol]                
                while  j < len(sentence):
                    if ( (isinstance(sentence[j],list)) and ((sentence[j][0] == "not")) and (sentence[j][1]==sentence[i][1]) ):
                        del(sentence[j])
                    else:
                        j = j + 1
            elif ((isinstance(sentence[i], list)) and (sentence[i][0] == "or")):    # case of a disjunction
                while  j < len(sentence):
                    equal = 0
                    flag = True
                    if ((isinstance(sentence[j], list)) and (sentence[j][0] == "or")):
                        if len(sentence[j]) == len(sentence[i]):
                            ii = 1
                            equal = 0
                            while(ii < len(sentence[i])):
                                jj = 1
                                while(jj< len(sentence[j])):
                                    if sentence[i][ii] == sentence[j][jj]:
                                        equal += 1    
                                    jj = jj + 1
                                ii = ii + 1
                            if(len(sentence[i])==len(sentence[j])==2):
                                sentence[j]=sentence[j][1]
                                sentence[i]=sentence[i][1]
                                flag = False
                                
                    if equal == len(sentence[j]) - 1 and flag and equal!=0:
                       # print ">>",equal
                        del(sentence[j])
                    else:
                        j = j + 1
            i = i + 1  
        if len(sentence) == 2:
            sentence = sentence[1]
        elif len(sentence) == 1:
            sentence = []
            print "Empty Sentence"
        if isinstance(sentence, list):
            if(len(sentence)==2):
                if sentence[0]==sentence[1]:
                    sentence=sentence[0]
    
    for i in range(len(sentence)):
        if isinstance(sentence[i], list):
            if(len(sentence[i])==2):
                if sentence[i][0]==sentence[i][1]:
                    sentence[i]=sentence[i][0]
                        
    return sentence


def postprocess(sentence):
    
    if isinstance(sentence, list):
        if(len(sentence)==2):
            if sentence[0]==sentence[1]:
                sentence=sentence[0]
    if isinstance(sentence, str):
        sentence = repr(sentence)
    return sentence


def CNF(sentence):
    
    sentence = Distributivity(sentence)
    sentence = AssociativityAND(sentence)
    sentence = AssociativityOR(sentence)
    sentence = Factor(sentence)

    return sentence
 
sentence=CNF(sentence)  
sentence = postprocess(sentence)

print sentence
import time
import random

# start_time = time.time()
filename="input.txt"
# filename="Samples-test-cases/input5.txt"
file = open(filename, "r")
content = file.read().splitlines()

# print content

firstLine=content[0].split()
noOfGuests= int(firstLine[0])
noOfTables= int(firstLine[1])
splitSymbol='#'
mainTAG="Main-Test: "

# print noOfGuests
# print noOfTables

sentence=[]
friendList=[]
enemyList=[]

for i in range(1,content.__len__(),1):
    line=content[i].split()
    tempList = [int(line[0]), int(line[1])]

    if (line[2]=='F'):
        friendList.append(tempList)

    elif (line[2]=='E'):
        enemyList.append(tempList)


    # print content[i]

# print mainTAG,"frind list is: " ,friendList
# print mainTAG,"enemy list is: " ,enemyList

tempSentence=[]
# For each guest a, the assignment should be at only one table

for i in range(1,noOfGuests+1,1):
    # clause = [];
    clause2 = []
    for j in range(1,noOfTables+1,1):

        # clause.append('x'+str(i)+splitSymbol+str(j))
        clause2.append('x' + str(i) +splitSymbol + str(j))
    tempSentence.append(clause2)

    # if noOfTables !=1 :
    #   sentence.append(clause)

# print mainTAG,"guest 1: ", tempSentence

for x in range(0,len(tempSentence),1):
    cGroup=tempSentence[x]
    for i in range(0,len(cGroup),1):
        symbol=cGroup[i]
        for j in range (i+1, len(cGroup),1):
            symbol2=cGroup[j]
            clause=[]
            clause.append('-'+symbol)
            clause.append('-'+symbol2)
            sentence.append(clause)

# print mainTAG, "guest : ", sentence

for i in range(1,noOfGuests+1,1):
    clause = [];

    for j in range(1,noOfTables+1,1):
        clause.append('x'+str(i)+splitSymbol+str(j))



    sentence.append(clause)



# print mainTAG,"guest/Table: ", sentence

# for enemines
for i in range(1,noOfTables+1,1):

    for j in range(0, enemyList.__len__(), 1):
        clause = [];
        a=enemyList[j][0]
        b=enemyList[j][1]
        clause.append('-x'+str(a)+ splitSymbol+ str(i))
        clause.append('-x' + str(b) +splitSymbol+ str(i))
        sentence.append(clause)

# print mainTAG,"enemies: ", sentence

# for friends
for i in range(1,noOfTables+1,1):

    for j in range(0, friendList.__len__(), 1):
        clausef = []
        secondClause = []
        a=friendList[j][0]
        b=friendList[j][1]
        clausef.append('-x'+str(a)+splitSymbol+str(i))
        clausef.append('x' + str(b) + splitSymbol+str(i))
        # print "clause first is: ", clausef

        secondClause.append('x' + str(a) +splitSymbol+ str(i))
        secondClause.append('-x' + str(b) + splitSymbol+str(i))

        # print "clause second is: ", secondClause
        sentence.append(clausef)
        sentence.append(secondClause)

# print mainTAG,"Full sentence: ", sentence


def isTautology(clause):
    # print clause
    for i in range(0, len(clause), 1):
        literal=clause[i]
        for j in range(0,len(clause),1):
            if literal=='-'+clause[j] and j!=i:
                # print literal,clause[j]
                return True

    return False

# clauseList=['-x1#1', 'x1#2','x3#2', 'x3#2','x1#1', 'x1#2']
# print mainTAG, "isTautology", isTautology(clauseList)

def discardTautololgies(sentence):
    # print len(sentence)
    newSentence=[]
    for i in range(0,len(sentence),1):

        if not isTautology(sentence[i]):
            # print i, sentence[i]
            # del sentence[i]
            newSentence.append(sentence[i])
        # else:
        #     newSentence.append(sentence[i])


    return newSentence
#
# testSententence=[['x1#1', 'x1#2','x3#2', 'x3#2','x1#1', 'x1#2'], ['-x1#1', 'x1#1'], ['-x2#2', 'x2#2'],['-x1#4', 'x1#4']]
# print  mainTAG, "discardTautololgies",discardTautololgies(testSententence)

def resolveNegativeWithPositive(ci,cj):
    # print "clasues",iclause,jclause
    # ci=iclause
    # cj=jclause

    # resolvedClauseSentence=[]

    for i in range(0,len(ci),1):
        x=ci[i]
        for j in range(0,len(cj),1):
            y=cj[j]
            if x=='-'+y :
                # ci.remove(x)
                # cj.remove(y)
                z=ci+cj
                z.remove(x)
                z.remove(y)
                # resolvedClauseSentence.append(z)

                return list(set(z))

    # for cj,ci
    # for j in range(0,len(cj),1):
    #     x=cj[j]
    #     for i in range(0,len(ci),1):
    #         y=ci[i]
    #         if x=='-'+y :
    #             z=ci+cj
    #             resolvedClauseSentence.append(z)
    # return resolvedClauseSentence

# print "resolveNegativeWithPositive" , resolveNegativeWithPositive(['-x1#1', 'x1#2'],['x1#1', '-x1#2'])

def plResolve(c1i,c2j):
   # print "ci,cj", resolveNegativeWithPositive(c1i,c2j)
   # print "cj,ci", resolveNegativeWithPositive(c2j,c1i)
   resolvedClauseSentence=[]
   r1= resolveNegativeWithPositive(c1i,c2j)
   r2= resolveNegativeWithPositive(c2j,c1i)
   if r1 is not None:
       resolvedClauseSentence.append(r1)
       # print r1
   if r2 is not None:
       resolvedClauseSentence.append(r2)
       # print r2

   return discardTautololgies(resolvedClauseSentence)

# test2=plResolve(['-p21','b11'],['-b11','p12','p21'])
# print "plResolve" , test2
# if test2==[]:
#     print "tuautolgy[]"
# elif test2==[[]]:
#     print "Emty set [[]]"

# x = []
# x.extend([[4], [5]])
# x.extend([[4], [5]])
# print (x)

# print set(['a','c']).issubset(['a','b','c'])

# one = [1, 2, 3]
# two = [4, 3, 2, 1]
#
# print all(x in two for x in one)

def plResolution(clausesSentence):
    newClauses=[]

    while True:
        sentence=list(clausesSentence)
        for i in range(0, len(sentence), 1):
            iClause=sentence[i]
            for j in range(i+1, len(sentence), 1):
                jClause= sentence[j]
                resolvents=plResolve(iClause,jClause)

                # if empty set
                if resolvents ==[[]]:
                    return False
                if resolvents != []:
                    newClauses.extend(resolvents)
                    # print resolvents

         # if new is subset of clausesSentences then return false
        # if set(newClauses).issubset(clausesSentence):
        if all(x in clausesSentence for x in newClauses):
            return True


        clausesSentence.extend(newClauses)





# print mainTAG, "plResolution",plResolution(sentence)

def getRandomAssignedModel():
    newList=[]
    for i in range(0,noOfGuests,1):
        guest=[]
        for j in range(0,noOfTables,1):
            if random.randint(0,9)>=5:
                guest.append(True)
            else:
                guest.append(False)
        newList.append(guest)

    return newList
# print mainTAG, "getRandomAssignedModel",getRandomAssignedModel()

def replaceSymbolsAndDiscardClauseIfTrue(sentence,value,symbol):
    newSentence=[]

    if value:
        compValue=False
    else:
        compValue=True

    for i in range(0,len(sentence),1):
        clause=list(sentence[i])
        for j in range(0,len(clause),1):
            if clause[j]==symbol:
                if value:
                    clause[j]=value
            elif clause[j]== '-'+symbol:
                if compValue:
                    clause[j]=compValue

        if True not in clause:
            newSentence.append(clause)

    return newSentence

# print mainTAG,"replaceSymbolsAndDiscardClauseIfTrue ", replaceSymbolsAndDiscardClauseIfTrue([['-x1#1'], ['x1#1', '-x2#2']],False,'-x1#1')
# symbol dependent
def satisfies(sentence, model):
    checkSentence=list(sentence)
    for i in range(1,noOfGuests+1,1):
        for j in range(1,noOfTables+1,1):
            checkSentence= replaceSymbolsAndDiscardClauseIfTrue(checkSentence, model[i-1][j-1], 'x'+str(i)+splitSymbol+str(j))


    # if checkSentence==[]:
    #     return True
    # else:
    #     return False
    return checkSentence

# print mainTAG,"satisfies ",satisfies(sentence,[[False, True], [False, True], [True, False], [True, False]])

# problem with following


def walkSat(sentence):
    TAG="walkSat:   "
    # print TAG, "Sentence is:    ", sentence
    model=getRandomAssignedModel()
    for x in range(0,10000,1):
    # while True:
    #     print TAG,"model is:    ", model
        copySentence=list(sentence)
        # print TAG, "copySentence is:    ", copySentence
        remainingClauses=satisfies(copySentence,model)
        # print TAG,"remainingClauses:    ", remainingClauses
        if remainingClauses==[]:
            return model

        clause=remainingClauses[random.randint(0,len(remainingClauses)-1)]
        symbol= clause[random.randint(0,len(clause)-1)]
        symbol=symbol.split('x')[1]
        i=int (symbol.split(splitSymbol)[0]) -1
        j=int (symbol.split(splitSymbol)[1]) -1
        # print TAG,"selected symbol",symbol,i, j,model[i][j]
        # flip the symbol
        if model[i][j]:
            model[i][j]=False
        else:
            model[i][j]=True

        # print TAG, "New model is:    ", model



def outputModel(model):
    for i in range(0,noOfGuests,1):
        for j in range(0,noOfTables,1):
            if model[i][j]:
                print "Guest: ",i+1," on Table: ", j+1


# outputModel(walkSat(sentence))

# walkSat(sentence)



def findPureSymbol(sentence):
    pSentence=list(sentence)
    newSet= set()
    for i in range(0,len(pSentence),1):
        pClause=pSentence[i]
        for j in range(0,len(pClause),1):
            newSet.add(pClause[j])

    # print newSet

    newList=list(newSet)
    pureSymbolList=list(newSet)
    for i in range(0, len(newList),1):
        # print newList[i]
        pSymbol=newList[i]
        for j in range(0,len(newList),1):
            if pSymbol=='-'+newList[j]:
                # print "pureSymbolList", pureSymbolList, newList[j], pSymbol
                pureSymbolList.remove(pSymbol)
                pureSymbolList.remove(newList[j])


    return pureSymbolList



# print "findPureSymbol",
# s=findPureSymbol([['x1#1', 'x1#2'], ['x1#1', '-x1#3'], ['-x1#2', '-x1#3']])
# s=findPureSymbol(sentence)
# print "s is",s

def findUnitClause (sentence):
    for i in range(0,len(sentence),1):
        if len(sentence[i])==1:
            return sentence[i][0]
# print findUnitClause([['x1#1', 'x1#2'], ['x1#1', '-x1#3'], ['-x1#3']])

def DiscardSymbolsFromClauses(sentence,symbol):
    newSentence=[]


    for i in range(0,len(sentence),1):
        clause=list(sentence[i])
        newClause=list()
        for j in range(0,len(clause),1):
            if clause[j]!=symbol:
                newClause.append(clause[j])


        newSentence.append(newClause)

    return newSentence

# print "DiscardSymbolsFromClauses",DiscardSymbolsFromClauses([['x1#1'], ['-x2#1', '-x2#1'], ['-x2#1', '-x3#2']],'-x2#1')



def getComplementarySymbol(symbol):
    if symbol[:1]=='-':
        compFirstSymbol=symbol[1:]
    else:
        compFirstSymbol='-'+symbol
    return compFirstSymbol


def dpll(sentence,model):

    if sentence==[]:
        return True,model
    if [] in sentence:
        return False
    # pure symbol
    pureSymbols=findPureSymbol(sentence)
    if len(pureSymbols)>0:
        for p in pureSymbols:
            sentence=replaceSymbolsAndDiscardClauseIfTrue(sentence,True,p)
            model.append(p);
    # run dpll again
    if len(sentence)==0 or len(sentence)==1:
        if len(sentence)==1:
            if len(sentence[0])==0:
                dpll(sentence,model)
        else:
            dpll(sentence,model)
    # unit clause
    unitClause=findUnitClause(sentence)
    if unitClause is not None:

        model.append(unitClause)
        sentence=replaceSymbolsAndDiscardClauseIfTrue(sentence,True,unitClause)
        sentence=DiscardSymbolsFromClauses(sentence,getComplementarySymbol(unitClause))


    # run dpll again
    if len(sentence)==0 or len(sentence)==1:
        if len(sentence)==1:
            if len(sentence[0])==0:
                dpll(sentence,model)
        else:
            dpll(sentence,model)

    if sentence==[]:
        return True,model
    if [] in sentence:
        return False
    firstSymbol=sentence[0][0]
    sentence1=list(sentence)
    sentence2=list(sentence)
    if firstSymbol[:1]=='-':
        compFirstSymbol=firstSymbol[1:]
    else:
        compFirstSymbol='-'+firstSymbol
    sentence1=replaceSymbolsAndDiscardClauseIfTrue(sentence1,True,firstSymbol)
    sentence1=DiscardSymbolsFromClauses(sentence1,compFirstSymbol)
    sentence2=replaceSymbolsAndDiscardClauseIfTrue(sentence2,True,compFirstSymbol)
    sentence2=DiscardSymbolsFromClauses(sentence2,firstSymbol)
    model1=list(model)
    model1.append(firstSymbol)
    model2=list(model)
    model2.append(compFirstSymbol)
    return dpll(sentence1,model1) or dpll(sentence2,model2)



def outputDpllModel(ansList):
    guestAnsList=list()
    for i in range(0, noOfGuests + 1, 1):
        guestAnsList.append(-1)
    for ans in ansList:
        if ans[:1] != '-':
            ans = ans.split('x')[1]
            i = int(ans.split(splitSymbol)[0])
            j = int(ans.split(splitSymbol)[1])
            guestAnsList[i]=j
    return guestAnsList

# print outputDpllModel(['-x1#1', 'x1#2', '-x2#1', 'x2#2', '-x3#1', 'x3#2', 'x4#1', '-x4#2', 'x5#1', '-x5#2'])

outFile = open("output.txt", "w")
# outFile.write(boardString)
# outFile.write(traversalLog)


def showAnsGuestList(guestList):
    for i in range(1,len(guestList),1):
        print i," ",guestList[i]
        outFile.write("\n"+str(i) +' '+str(guestList[i]))


ansDpll = dpll(sentence, [])
if type(ansDpll) is not bool:
    if ansDpll[0]:
        print "yes"
        outFile.write("yes")
        showAnsGuestList(outputDpllModel(ansDpll[1]))
else:
    print "no"
    outFile.write("no")

outFile.close()
# print "time elapsed: {:.2f}s".format(time.time() - start_time)
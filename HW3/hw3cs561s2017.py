import time
import copy

# start_time = time.time()


# filename="input.txt"
filename="sample/input39.txt"
file = open(filename, "r")
content = file.read().splitlines()

# print content
mainTAG="Main-Test: "
queryLines=True
nodeLines=False
queries=list()
listOfTables=list()
table = list()

for i in range(0,len(content),1):
    # print content[i]
    if(queryLines):
        if content[i] == "******":
            queryLines=False
            nodeLines=True
            nodeHeadLine=True
        else:
         queries.append(content[i])


    elif nodeLines:

        if content[i] =="***" or content[i] =="******" :
            listOfTables.append(table)
            table= list();
        else:
            table.append(content[i])

listOfTables.append(table)


# print queries
class Query:
    def __init__(self,type,queries,evidence):
        self.type=type
        self.queries =queries
        self.evidence = evidence

queryList=list()
# print listOfTables
for i in range(0,len(queries),1):
    type=''
    qdict=dict()
    edict=dict()
    qlist=list()

    # P(E = -, G = - | A = -, C = +)
    qt=queries[i].split('(')
    # P
    type=qt[0]

    if type == "P" or type == "EU":
        # E = -, G = - | A = -, C = +)
        qe = qt[1].split(' | ')
        # E = -, G = -
        qParts = qe[0].split(', ')
        for j in range(0, len(qParts), 1):
            # E = -
            elements = qParts[j].split(' = ')
            qdict[elements[0]] = elements[1].split(')')[0]
        if len(qe) == 2:
            # A = -, C = +)
            eParts= qe[1].split(', ')
            for j in range(0, len(eParts), 1):
                # E = -
                elements = eParts[j].split(' = ')
                edict[elements[0]] = elements[1].split(')')[0]
        q=Query(type,qdict,edict)
        queryList.append(q)
    elif type == 'MEU':
        # MEU(I)
        # MEU(I | L = +)
        # MEU(I, L)
        qe2=qt[1].split(' | ')
        if len(qe2) == 2:
            qs1=qe2[0].split(', ')
            qlist.extend(qs1)
            qs2 = qe2[1].split(', ')
            for j in range(0, len(qs2), 1):
                # E = -
                element = qs2[j].split(' = ')
                edict[element[0]] = element[1].split(')')[0]
        else:
            es = qe2[0].split(', ')
            for j in range(0,len(es),1):
                qlist.append(es[j].split(')')[0])
        q = Query(type, qlist, edict)
        queryList.append(q)


def printQueryList():
    print "Query length : ", len(queryList), "--   "
    for i in range(0,len(queryList),1):
        q=queryList[i]
        print "Query : ",i+1,"--   "
        print "type: ", q.type
        print "queries: ", q.queries
        print "evidence: ", q.evidence


# printQueryList()



class Node:
    def __init__(self,name,type,parents,probabilities):
        self.name=name
        self.type=type
        self.parents=parents
        self.probabilities = probabilities

listOfNodes=list()
listOfNodeNames=list()


for i in range(0, len(listOfTables), 1):
    node=listOfTables[i]
    # print node
    headline=node[0].split(' ')
    # print headline
    name = headline[0]
    if name != "utility":
        listOfNodeNames.append(name)
    if len(headline) == 1:
        # root node or decision node
         if node[1] == "decision":
            # print node[1]
            type="decision"
            n = Node(name, type, [], {})

         else:
             type="root"
             prob={name:node[1]}
             n = Node(name, type, [], prob)
         listOfNodes.append(n)
    else:

        parents=list()
        prob = dict()
        prob[headline[0]]=node[0].split('|')[1].lstrip(' ')
        for j in range(2, len(headline), 1):
            parents.append(headline[j])
        for k in range(1,len(node),1):
            rowParts = node[k].split(' ',1)
            prob[rowParts[1]]=rowParts[0]
        if name == "utility":
            type = "utility"
        else:
            type="node"
        # print parents,prob
        n= Node(name,type,parents,prob)
        listOfNodes.append(n)
def printNode(n):
    print ".......NODE......."
    print "name: ",n.name
    print "type: ",n.type
    print "probabilities",n.probabilities
    print "parents",n.parents

# for i in range(0,len(listOfNodes),1):
#     n=listOfNodes[i]
#     print "------- ",i," ------------"
#     printNode(n)
#     print



def getNodeFromName(nodeName):
    for i in range(0,len(listOfNodes),1):
        if nodeName == listOfNodes[i].name:
            return listOfNodes[i]
# ns=getNodeFromName("A")
# printNode(ns)



#  G    {'A': '-', 'C': '+', 'B': '-', 'E': '-', 'D': '-', 'G': '-', 'F': '+'}
def getProbability(probOf,allVars):
    # print "all vars", allVars
    node=getNodeFromName(probOf)
    parentsCombination=""
    for i in range(0,len(node.parents),1):
        sign= allVars.get(node.parents[i])
        parentsCombination+=" "+sign

    if node.type=="node":
        positvieProb=node.probabilities.get(parentsCombination.lstrip(' '))
    elif node.type == "root":
        positvieProb = node.probabilities.get(node.name)
    elif node.type == "decision":
        # print "getProbability",probOf,allVars
        # return node.probabilities.get(node.type)
        probOfSign = allVars.get(probOf)
        if probOfSign == '+':
            return 1.0
        elif probOfSign == '-':
            return 1.0

    elif node.type == "utility":
        return 1.0



    probOfSign = allVars.get(probOf)
    if probOfSign == '-':
        return 1.0 - float(positvieProb)
    elif probOfSign == '+':
        return float(positvieProb)



# print getProbability('E',{'A': '+', 'C': '+', 'B': '-', 'E': '-', 'D': '-', 'G': '-'})
# print getProbability('C',{'A': '-', 'C': '+', 'B': '-'})
# print getProbability('A',{'A': '+', 'C': '+', 'B': '+'})


def enumerateAll(vars,e):
    # print "-----------------e is : ", e
    if len(vars) == 0:
        return 1.0
    y=vars[0]

    # currentNode=getNodeFromName(y)

    if y in e:
        return getProbability(y,e) * enumerateAll(vars[1:], e)
    else:
        eWithyPositve= copy.deepcopy(e)
        eWithyPositve[y]='+'

        eWithyNegative = copy.deepcopy(e)
        eWithyNegative[y] = '-'
        return getProbability(y , eWithyPositve) * enumerateAll(vars[1:], eWithyPositve) + getProbability(y,eWithyNegative) * enumerateAll(vars[1:], eWithyNegative)


# print enumerateAll(['A', 'B', 'C'],{'A': '+', 'C': '+'})
# print enumerateAll(['A', 'B', 'C', 'D', 'E', 'F', 'G'],{'A': '-', 'C': '+', 'E': '+', 'G': '-'})
# print "----------------------------------------------------"
# e={'A': '+', 'C': '+'}
# var= ['A', 'B', 'C']
# y=var[1]
# print 'y ', y
# ey=copy.deepcopy(e)
# ey[y]="-"
# et=copy.deepcopy(e)
# et[y]="+"
# print 'ey ', ey
# print 'et ', et


def mapCombination(combination,query):
    d=dict()

    for i in range(0,len(combination),1):
        if combination[i] == '1':
            d[query[i]]='+'
        elif combination[i] == '0':
            d[query[i]]='-'

    return d

# print mapCombination(['1', '1', '1'],['A','B','C'])

def enumerationAsk(x,e,bnNodes):
    # print '-----------X is: ', x, "e is ", e
    newX=copy.deepcopy(x)



    for key in newX.keys():
        keyNode=getNodeFromName(key)
        if(keyNode.type=="decision") and (e[key]!=newX[key]):
            # print "key",key
            return 0.0
        elif keyNode.type=="decision":
            # print "key",key
            newX.pop(key,None)
            # print newX

    enumerateList = list()
    queryEn = 0
    queryList = newX.keys()

    for i in range(0, 2 ** len(queryList)):
       qComb= mapCombination((list(bin(i)[2:].zfill(len(queryList)))),queryList)
       # eWithqComb=copy.deepcopy(e)
       eWithqComb=dict(qComb.items() + copy.deepcopy(e).items())
       enumerate = enumerateAll(bnNodes, eWithqComb)
       enumerateList.append(enumerate)
       if qComb == newX:
            # print "qComb; ", qComb
            queryEn=i

    # eWithq = dict(x.items() + copy.deepcopy(e).items())

    # print "eq: ",enumerateList[queryEn]/sum(enumerateList)
    # print "enumerateList: ", enumerateList
    # print "sum",sum(enumerateList)
    return enumerateList[queryEn]/sum(enumerateList)


#                   query     evidence    all vars in baysnet
# enumerationAsk({'A': '-'}, {'C': '+'},['A','B','C'])
# print enumerationAsk({'E': '-', 'G': '-'}, {'A': '-', 'C': '+'},listOfNodeNames)

# print listOfNodeNames


# t={'E': '-', 'G': '-'}
# x={'F': '+', 'H': '-'}
# print dict(t.items() + x.items())

# def per(n):
#     for i in range(1<<n):
#         s=bin(i)[2:]
#         s='0'*(n-len(s))+s
#         print map(int,list(s))
# per(3)
#
# listLength=3
# for x in range(0,2**listLength):
#     print(list(bin(x)[2:].zfill(listLength)))



# class Factor:
#     def __init__(self,name,vars,probabilities):
#         self.name=name
#         self.vars=vars
#         self.probabilities = probabilities
#
# def makeFactor(node,e):
#     lengthOfParents=len(node.parents)
#     factorProb=[]
#     for x in range(0,2**lengthOfParents):
#         qComb = mapCombination((list(bin(i)[2:].zfill(len(lengthOfParents)))), node.parents)
#
#     pass
#
# #                   query     evidence
# # makeFactor(listOfNodes[2],{'A': '-','C':'+'})
#
# def eliminationAsk(x,e,bn):
#     factors=[]
#     print "x is: ", x,"e is: ",e
#     for i in range(len(listOfNodes)-1,-1,-1):
#         print listOfNodes[i].name
#
#
#
# eliminationAsk(queryList[0].queries,queryList[0].evidence,listOfNodes)

def getUtilityNode():
    for i in range(len(listOfNodes)-1,-1,-1):
        # print i
        if listOfNodes[i].type == "utility":
            return listOfNodes[i]

# print getUtilityNode().parents

#  {'E': '-', 'G': '+', 'F': '-'}
def getUtility(utilityNode,utilityParentsDict):

    utilityParentsList=utilityNode.parents
    parentsCombination = ""
    for i in range(0, len(utilityParentsList), 1):
        sign = utilityParentsDict.get(utilityParentsList[i])

        parentsCombination += " " + sign
    return float(utilityNode.probabilities.get(parentsCombination.lstrip(' ')))

# print getUtility(getUtilityNode(),{'E': '+', 'G': '+', 'F': '+'})

def ExpectedUtilityAsk(evidence):
    utilityNode=getUtilityNode()
    # evidence=dict(Query.queries.items() + Query.evidence.items())
    queryList=utilityNode.parents
    utility=0
    for i in range(0, 2 ** len(queryList)):
       qComb= mapCombination((list(bin(i)[2:].zfill(len(queryList)))),queryList)
       # print qComb,getUtility(utilityNode,qComb)
       utility=utility+enumerationAsk(qComb,evidence,listOfNodeNames)*getUtility(utilityNode,qComb)
    return utility
#
# def setDecisionNodeProb(ev):
#     for i in range(0,len(listOfNodes),1):
#         if listOfNodes[i].type =="decision":
#             if ev.get(listOfNodes[i].name)=='+':
#                 listOfNodes[i].probabilities["decision"]=1.0
#             else:
#                 listOfNodes[i].probabilities["decision"] = 0.0
anslist=list()
for i in range(0,len(queryList),1):
    q=queryList[i]
    if q.type == "P":
        a=format(enumerationAsk(q.queries, q.evidence, listOfNodeNames),'.2f')
          # format(1.2345, '.2f')
        # print "Ans is------------------: ",i, a
        anslist.append(a)
    elif q.type == "EU":
        # print q.queries,q.evidence
        evidence=dict(q.queries.items() + q.evidence.items())
        # evidence=setDecisionNodeProb(evidence)
        e=int(round(ExpectedUtilityAsk(evidence),0))
        # print "evidnece is ",evidence
        # print "Ans is------------------: ",i,e
        anslist.append(e)
    elif q.type == "MEU":
        qlist = q.queries
        maxUtility = 0
        ans={}
        for i in range(0, 2 ** len(qlist)):
            qComb = mapCombination((list(bin(i)[2:].zfill(len(qlist)))), qlist)
            evidence = dict(qComb.items() + q.evidence.items())
            eu=ExpectedUtilityAsk(evidence)
            if eu>maxUtility:
                maxUtility=eu
                ans=qComb
        meuAns=""
        for j in range(0,len(qlist),1):
            meuAns=meuAns+ans.get(qlist[j])+" "
        meuAns+=str(int(round(maxUtility,0)))
        anslist.append(meuAns)
# print "ANS LIST: ",anslist
outFile = open("output.txt", "w")
for i in range(0,len(anslist),1):
    print anslist[i]
    outFile.write(str(anslist[i]))
    if i< len(anslist)-1:
        outFile.write("\n")
outFile.close()
# print "time elapsed: {:.2f}s".format(time.time() - start_time)
# print "hello humayoun"
global traversalLog
global depth,passTurn
def printBoard(n):
    print '    a ,  b ,  c ,  d ,  e ,  f ,  g ,  h  '
    print '    0 ,  1 ,  2 ,  3 ,  4 ,  5 ,  6 ,  7  '
    l = 0
    for i in n:
        print (l),
        print i,l+1
        l += 1

def converBoardToSring(n):
    b=''
    for i in range(0,8,1):
        b=b+"".join(n[i])
        b=b+'\n'
    return b

filename="FinalTestCasesHW1/input21.txt"
# filename="TestCases/TestCase1/input.txt"
# filename="TestCases/TestCase2/input.txt"
# filename="TestCases/TestCase3/input.txt"
# filename="TestCases/TestCase4/input.txt"
# filename="TestCases/TestCase5/input.txt"
# filename="TestCases/TestCase6/input.txt"

with open(filename, "r+b") as f:
    content = f.read().splitlines()

# print content
playerToMove= content[0]
searchCutOffDepth = int(content[1])

# print playerToMove
# print searchCutOffDepth
startBoardStatus=[]
for i in range(2,10,1):
    startBoardStatus.append(list(content[i]))


# printBoard(startBoardStatus)

positionalBoardWeights =[ [99, -8, 8, 6, 6, 8, -8, 99],
                    [-8, -24, -4, -3, -3, -4, -24, -8],
                          [8, -4, 7, 4, 4, 7, -4, 8],
                          [6, -3, 4, 0, 0, 4, -3, 6],
                          [6, -3, 4, 0, 0, 4, -3, 6],
                          [8, -4, 7, 4, 4, 7, -4, 8],
                          [-8, -24, -4, -3, -3, -4, -24, -8],
                          [99, -8, 8, 6, 6, 8, -8, 99]]

#print positionalBoardWeights
def getOpponent(player):
    if player == 'X':
        return'O'
    else:
        return'X'

opponentPlayer=getOpponent(playerToMove);

def evaluateWeight(player, oppPlayer, curruntBoard):
    playerWeight = 0
    oppPlayerWeight = 0

    for i in range(0, 8, 1):
        for j in range(0, 8, 1):
            if curruntBoard[i][j]==player:
                playerWeight = playerWeight + positionalBoardWeights[i][j]
            elif curruntBoard[i][j]==oppPlayer:
                oppPlayerWeight= oppPlayerWeight+ positionalBoardWeights[i][j]

    return playerWeight - oppPlayerWeight



moveRight=(0,1)
moveLeft=(0,-1)
moveTop=(-1,0)
moveBottom=(1,0)
moveTopRight=(-1,1)
moveTopLeft=(-1,-1)
moveBottomRight=(1,1)
moveBottomLeft=(1,-1)
possibleDirectionsToMove = [moveTopLeft, moveTop, moveTopRight,moveLeft,moveRight,moveBottomLeft, moveBottom, moveBottomRight]

def moveInPossibleDirection(currentPositionX,currentPositionY,direction):

    currentPositionX=currentPositionX+direction[0]
    currentPositionY=currentPositionY+direction[1]

    if (currentPositionX<0):
        return False
    elif (currentPositionX>=8):
        return False
    elif (currentPositionY<0):
        return False
    elif (currentPositionY>=8):
        return False
    else:
        return (currentPositionX, currentPositionY)




def nextPossibleMoves(player,opponent, boardStatus):


    possibleMoves = []
    for i in range(0,8,1):
        for j in range(0,8,1):
            if boardStatus[i][j] == '*':
                for direction in possibleDirectionsToMove: # 8 possible directions to move

                    nextPossibleMove = moveInPossibleDirection(i, j, direction)

                    if (nextPossibleMove) and (boardStatus[nextPossibleMove[0]][nextPossibleMove[1]] == opponent):

                        while boardStatus[nextPossibleMove[0]][nextPossibleMove[1]] == opponent:

                            nextPossibleMove = moveInPossibleDirection(nextPossibleMove[0],nextPossibleMove[1], direction)
                            if (not nextPossibleMove):
                                break

                            elif boardStatus[nextPossibleMove[0]][nextPossibleMove[1]] == player:
                                possibleMoves.append((i, j))
                                break



    return possibleMoves


def makeMove(player,opponent,boardStatus,move):

    newboard=[]
    for i in range(0,8,1):
        newboard.append(list(boardStatus[i]))


    # print newboard

    for i in range(0,8,1):

        for j in range(0,8,1):

            if (boardStatus[i][j] == '*') and ((i,j)==move):
                newboard[move[0]][move[1]] = player
                for direction in possibleDirectionsToMove: # 8 possible directions to move
                    nextPossibleMove = moveInPossibleDirection(i, j, direction)
                    if (nextPossibleMove) and (boardStatus[nextPossibleMove[0]][nextPossibleMove[1]] == opponent):
                        flip=False
                        flipNextPossibleMove=nextPossibleMove
                        while boardStatus[nextPossibleMove[0]][nextPossibleMove[1]] == opponent:
                            nextPossibleMove = moveInPossibleDirection(nextPossibleMove[0],nextPossibleMove[1], direction)
                            if (not nextPossibleMove):
                                break

                            elif boardStatus[nextPossibleMove[0]][nextPossibleMove[1]] == player:
                                # possibleMoves.append((i, j))
                                flip=True
                                break

                        if (flip):
                            # print flipNextPossibleMove
                            while boardStatus[flipNextPossibleMove[0]][flipNextPossibleMove[1]] == opponent:
                                #print flipNextPossibleMove
                                newboard[flipNextPossibleMove[0]][flipNextPossibleMove[1]] = player
                                flipNextPossibleMove = moveInPossibleDirection(flipNextPossibleMove[0], flipNextPossibleMove[1],
                                                                           direction)

                                if boardStatus[flipNextPossibleMove[0]][flipNextPossibleMove[1]] == player:
                                    # possibleMoves.append((i, j))
                                    flip = True
                                    break


    # b=''
    # for i in range(0,8,1):
    #     b=b+"".join(newboard[i])

    return newboard

def getNode((i,j)):
    r=['1','2','3','4','5','6','7','8']
    c=['a','b','c','d','e','f','g','h']
    return c[j]+r[i]

# print nextPossibleMoves('X',getOpponent('X'), startBoardStatus)

def maxValue(player,opponent, boardState, alpha, beta,node):
    functionName=" ::MAX: "
    # print functionName+'In maxValue function',
    global traversalLog,depth,passTurn
    currentNode=node
    depth=depth+1
    value = -9999
    if depth >= searchCutOffDepth or passTurn>=2:


        if player==playerToMove:
            value = evaluateWeight(player, opponent, boardState)
        else:
            value = evaluateWeight(opponent, player, boardState)

        traversalLog = traversalLog + str(node) + ',' + str(depth) + ',' + str(
            value) + ',' + str(alpha) + ',' + str(beta) + '\n'
        depth=depth-1
        return value, boardState


    traversalLog = traversalLog + str(node) + ',' + str(depth) + ',' + str(
        value) + ',' + str(alpha) + ',' + str(beta) + '\n'

    moves= nextPossibleMoves(player,opponent,boardState)
    if len(moves)==0:
        # print functionName+'no moves'

        passTurn=passTurn+1

        value = max(value, minValue(opponent, player, boardState, alpha, beta, 'pass')[0])
        # print functionName+"value back is:;;;",
        # print value

        if value >= beta:
            traversalLog = traversalLog + node + ',' + str(depth) + ',' + str(
                value) + ',' + str(alpha) + ',' + str(beta) + '\n'
            depth = depth - 1
            return value, boardState

        alpha = max(alpha, value)
        traversalLog = traversalLog + node + ',' + str(depth) + ',' + str(
            alpha) + ',' + str(alpha) + ',' + str(beta)+ '\n'

        depth = depth - 1




        return value, boardState

    passTurn=0
    # print moves
    for move in moves:
        node=getNode(move)
        nextBoardState = makeMove(player, opponent, boardState, move)
        value= max(value,minValue(opponent,player, nextBoardState,alpha,beta,node)[0])

        if value >= beta:
            traversalLog = traversalLog + str(currentNode) + ',' + str(depth) + ',' + str(
                value) + ',' + str(alpha) + ',' + str(beta) + '\n'
            depth = depth - 1
            return value,nextBoardState

        alpha = max(alpha, value)
        traversalLog = traversalLog + str(currentNode) + ',' + str(depth) + ',' + str(
            value) + ',' + str(alpha) + ',' + str(beta) + '\n'

    depth = depth - 1
    # return alpha,nextBoardState
    return value,nextBoardState

def minValue(player, opponent, boardState, alpha, beta,node):
    functionName=" :: MIN: "
    # print functionName+'In minValue function'
    global traversalLog,depth,passTurn
    depth=depth+1
    currentNode=node

    value = 9999
    if (depth >= searchCutOffDepth or passTurn>=2):

        if player==playerToMove:
            value = evaluateWeight(player, opponent, boardState)
        else:
            value = evaluateWeight(opponent, player, boardState)

        traversalLog = traversalLog + str(node) + ',' + str(depth) + ',' + str(
            value) + ',' + str(alpha) + ',' + str(beta) + '\n'
        depth = depth - 1
        return value, boardState


    traversalLog = traversalLog + str(node) + ',' + str(depth) + ',' + str(
        value) + ',' + str(alpha) + ',' + str(beta) + '\n'

    moves = nextPossibleMoves(player, opponent, boardState)
    if len(moves) == 0:
        # print functionName+'no moves'

        passTurn=passTurn+1

        value = min(value, maxValue(opponent, player, boardState, alpha, beta, 'pass')[0])
        # value =  maxValue(opponent, player, boardState, alpha, beta, 'pass')[0]

        if value <= alpha:
            traversalLog = traversalLog + node + ',' + str(depth) + ',' + str(
                value) + ',' + str(alpha) + ',' + str(beta) + '\n'
            depth = depth - 1
            # return value, boardState
            return alpha, boardState

        beta = min(beta, value)

        traversalLog = traversalLog + node + ',' + str(depth) + ',' + str(
            value) + ',' + str(alpha) + ',' + str(beta) + '\n'

        depth = depth - 1


        return value, boardState

    passTurn=0
    # print moves
    for move in moves:
        node = getNode(move)
        nextBoardState = makeMove(player, opponent, boardState, move)

        value = min(value, maxValue(opponent, player, nextBoardState, alpha, beta,node)[0])

        beta = min(beta, value)
        if value <= alpha:
            traversalLog = traversalLog + str(currentNode) + ',' + str(depth) + ',' + str(
                alpha) + ',' + str(alpha) + ',' + str(beta) + '\n'
            depth = depth - 1
            # return value, nextBoardState
            return alpha, nextBoardState



        traversalLog = traversalLog + str(currentNode) + ',' + str(depth) + ',' + str(
            value) + ',' + str(alpha) + ',' + str(beta) + '\n'


    depth = depth - 1
    # return beta, nextBoardState
    return value, nextBoardState


def alphaBetaSearch(board):
    functionName="alphaBetaSearch"
    global traversalLog,depth,passTurn
    passTurn=0
    depth=0
    alpha=-9999
    beta=9999
    value=-9999

    traversalLog = "Node,Depth,Value,Alpha,Beta" + '\n'
    traversalLog = traversalLog+ 'root' + ',' + str(depth) + ',' + str(value) + ',' + '-9999' + ',' + '9999' + '\n'

    moves = nextPossibleMoves(playerToMove, getOpponent(playerToMove), board)
    # print moves

    if len(moves)==0:
        # print functionName+'no moves'

        passTurn=passTurn+1


        value = max(value, minValue(getOpponent(playerToMove), playerToMove, board, alpha, beta, 'pass')[0])


        if value >= beta:
            traversalLog = traversalLog + 'root' + ',' + str(depth) + ',' + str(
                value) + ',' + str(alpha) + ',' + str(beta) + '\n'
            depth = depth - 1
            return board

        alpha = max(alpha, value)
        traversalLog = traversalLog + 'root' + ',' + str(depth) + ',' + str(
            alpha) + ',' + str(alpha) + ',' + str(beta) + '\n'

        depth = depth - 1




        return board


    bestvalue=-9999999999
    for move in moves:
        node = getNode(move)
        nextBoardState = makeMove(playerToMove, getOpponent(playerToMove), board, move)
        # printBoard(nextBoardState)
        results=minValue(getOpponent(playerToMove),playerToMove, nextBoardState,alpha,beta,node)
        alpha = max(alpha, results[0])
        beta = max(beta, results[0])
        traversalLog = traversalLog+ 'root' + ',' + str(depth) + ',' + str(results[0]) + ',' + str(alpha) + ',' + str(beta) + '\n'
        # nb=nextBoardState
        if(results[0]>bestvalue):
            bestvalue=results[0]
            # print functionName + "best value is: ------------------------------------------------" + str(bestvalue)
            # printBoard(nextBoardState)
            nb=nextBoardState

    return nb # nextstateboard

b=alphaBetaSearch(startBoardStatus)
traversalLog = traversalLog.replace("-9999", "-Infinity")
traversalLog = traversalLog.replace("9999", "Infinity")

# printBoard(b)
boardString=converBoardToSring(b)

print boardString,
print traversalLog

outFile = open("output.txt", "w")
outFile.write(boardString)
outFile.write(traversalLog)
outFile.close()

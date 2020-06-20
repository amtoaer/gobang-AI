# ai.py
# coding = UTF-8
listAI = []
listHuman = []
listAIAndHuman = []
list_all = []
# AI下一步最应该下的位置
next_point = [0, 0]
# 棋盘大小
COLUMN = 15
ROW = 15
# 决策树深度（此处为2，但2步预测棋力其实很低）
DEPTH = 2
# 防守系数，系数越高，ai下的越保守
defend = 2


def ai(listAI, listHuman, list_all):
    """
    AI计算落子位置
    """
    # 先手第一步下在最中间
    if len(listHuman) == 0:
        next_point[0] = 7
        next_point[1] = 7
    else:
        # 将listAI与listHuman加入到listAIAndHuman
        listAIAndHuman = listAI+listHuman
        maxmin(True, DEPTH, -99999999, 99999999, listAI,
               listHuman, listAIAndHuman, list_all)
    return next_point[0], next_point[1]


def maxmin(is_ai, depth, alpha, beta, listAI, listHuman, listAIAndHuman, list_all):
    global next_point
    """
    负值极大算法搜索 alpha + beta剪枝
    """
    # 游戏是否结束||探索的递归深度是否到边界
    if game_win(listAI) or game_win(listHuman) or depth == 0:
        return evaluation(is_ai, listAI, listHuman)

    # 返回邻居点
    tmpList = getBlankList(listAIAndHuman)
    # 进行排序，排序后blank_list内靠前的节点是分数较高的节点，这样排序后（应该）可以增加剪枝效率
    blank_list = order(is_ai, tmpList, listAI, listHuman)

    # 遍历空点
    next_step = (0, 0)
    for next_step in blank_list:
        # 将空点加入对应位置
        if is_ai:
            listAI.append(next_step)
        else:
            listHuman.append(next_step)
        listAIAndHuman.append(next_step)
        # 预测另一方结果（每次递归深度-1）
        value = -maxmin(not is_ai, depth - 1, -beta, -alpha,
                        listAI, listHuman, listAIAndHuman, list_all)
        # 移除空点
        if is_ai:
            listAI.remove(next_step)
        else:
            listHuman.remove(next_step)

        listAIAndHuman.remove(next_step)
        if value > alpha:
            if depth == DEPTH:
                next_point = [next_step[0], next_step[1]]
            if value >= beta:
                return beta
            alpha = value
    return alpha


def getBlankList(listAIAndHuman):
    # 得到当前棋子周围的所有空点
    result = set()
    for node in listAIAndHuman:
        result = result | getNeighbor(node)
    return list(result-set(listAIAndHuman))


def getNeighbor(node):
    # 得到单个棋子周围的所有空点
    result = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            x = node[0] + i
            y = node[1]+j
            if inBoard(x, y):
                result.add((x, y))
    return result


def inBoard(x, y):
    # 判断(x,y)是否在棋盘上
    if x >= 0 and x <= COLUMN and y >= 0 and y <= ROW:
        return True
    return False


def order(isAI, blankList, listAI, listHuman):
    # 启发式搜索
    tmp = dict()
    if isAI:
        myList, enemyList = listAI, listHuman
    else:
        myList, enemyList = listHuman, listAI
    for node in blankList:
        # 对该点四个方向进行评估，并按照分数大小排序
        myScore = getNodeScore(node[0], node[1], myList, enemyList)
        tmp[node] = myScore
    return [item[0] for item in sorted(tmp.items(), key=lambda item: item[1], reverse=True)]


def evaluation(is_ai, listAI, listHuman):
    """
    评估函数
    """
    if is_ai:
        my_list = listAI
        enemy_list = listHuman
    else:
        my_list = listHuman
        enemy_list = listAI
    myScore = enemyScore = 0
    for node in my_list:
        myScore += getNodeScore(node[0], node[1], my_list, enemy_list)
    for node in enemy_list:
        enemyScore += getNodeScore(node[0], node[1], enemy_list, my_list)
    return myScore - enemyScore * defend


def getNodeScore(x, y, myList, enemyList):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    score = 0
    for direction in directions:
        score += getLineScore(x, y,
                              direction,  myList, enemyList)
    return score


def getLine(x, y, direction, myList, enemyList):
    line = [0 for i in range(9)]
    tmpX = x + (-5 * direction[0])
    tmpY = y + (-5 * direction[1])
    # 0为空棋子，1为我方棋子，2为敌方棋子
    for i in range(9):
        tmpX += direction[0]
        tmpY += direction[1]
        if (tmpX, tmpY) in myList:
            line[i] = 1
        elif (not inBoard(tmpX, tmpY)) or ((tmpX, tmpY) in enemyList):
            line[i] = 2
    return line


def getLineScore(x, y, direction, myList, enemyList):
    # 重构的单点得分函数
    line = getLine(x, y, direction, myList, enemyList)
    leftIndex, rightIndex = 4, 4
    # 判断我方棋子连续的长度
    while rightIndex < 8:
        if line[rightIndex + 1] != 1:
            break
        rightIndex += 1
    while leftIndex > 0:
        if line[leftIndex - 1] != 1:
            break
        leftIndex -= 1
    leftRange, rightRange = leftIndex, rightIndex
    # 延伸直到遇到敌方棋子
    while rightRange < 8:
        if line[rightRange + 1] == 2:
            break
        rightRange += 1
    while leftRange > 0:
        if line[leftRange - 1] == 2:
            break
        leftRange -= 1
    chessRange = rightRange - leftRange + 1
    # 形不成棋型（举例：201112，是完全没有意义的棋）
    if chessRange < 5:
        return 0
    myRange = rightIndex - leftIndex + 1
    count = dict.fromkeys(
        ['two', 'stwo', 'three', 'sthree', 'four', 'sfour', 'five'], 0)
    # 11111
    if myRange == 5:
        count['five'] += 1
    elif myRange == 4:
        left = line[leftIndex - 1]
        right = line[rightIndex + 1]
        # 011110
        if not (left or right):
            count['four'] += 1
        # 011112|211110
        elif not (left and right):
            count['sfour'] += 1
    elif myRange == 3:
        flag = False
        # 101112
        if line[leftIndex - 1] == 0 and line[leftIndex - 2] == 1:
            count['sfour'] += 1
            flag = True
        # 111012
        if line[rightIndex + 1] == 0 and line[rightIndex + 2] == 1:
            count['sfour'] += 1
            flag = True
        if not flag:
            if not (line[leftIndex - 1] or line[rightIndex + 1]):
                # 011100|001110
                if chessRange > 5:
                    count['three'] += 1
                # 2011102
                else:
                    count['sthree'] += 1
            elif not (line[leftIndex - 1] and line[rightIndex + 1]):
                count['sthree'] += 1
    elif myRange == 2:
        leftFlag, rightFlag = False, False
        leftEmpty, rightEmpty = False, False
        if line[leftIndex - 1] == 0:
            if line[leftIndex - 2] == 1:
                if line[leftIndex - 3] == 0:
                    leftFlag = True
                    if line[rightIndex + 1] == 0:
                        # 010110
                        count['three'] += 1
                    else:
                        # 010112
                        count['sthree'] += 1
                elif line[leftIndex - 3] == 2:
                    if line[rightIndex + 1] == 0:
                        # 210110
                        count['sthree'] += 1
                        leftFlag = True
            leftEmpty = True

        if line[rightIndex + 1] == 0:
            if line[rightIndex + 2] == 1:
                if line[rightIndex + 3] == 1:
                    # 11011
                    count['sfour'] += 1
                    rightFlag = True
                elif line[rightIndex + 3] == 0:
                    if leftEmpty:
                        # 011010
                        count['three'] += 1
                    else:
                        # 211010
                        count['sthree'] += 1
                    rightFlag = True
                elif leftEmpty:
                    # 011012
                    count['sthree'] += 1
                    rightFlag = True
            rightEmpty = True
        if leftFlag or rightFlag:
            pass
        elif leftEmpty and rightEmpty:
            # 0110
            count['two'] += 1
        elif leftEmpty or rightEmpty:
            # 2110|0112
            count['stwo'] += 1
    elif myRange == 1:
        leftEmpty = False
        if line[leftIndex - 1] == 0:
            if line[leftIndex - 2] == 1:
                if line[leftIndex - 3] == 0 and line[rightIndex + 1] == 2:
                    # 01012
                    count['stwo'] += 1
            leftEmpty = True
        if line[rightIndex + 1] == 0:
            if line[rightIndex + 2] == 1:
                if line[rightIndex + 3] == 0:
                    if leftEmpty:
                        # 01010
                        count['two'] += 1
                    else:
                        # 21010
                        count['stwo'] += 1
            elif line[rightIndex + 2] == 0:
                if line[rightIndex + 3] == 1 and line[rightIndex + 4] == 0:
                    if leftEmpty:
                        # 010010
                        count['two'] += 1
                    else:
                        # 210010
                        count['stwo'] += 1
    score = count['five']*100000+count['four']*10000+count['sfour']*1000 + \
        count['three']*1000+count['sthree']*100 + \
        count['two']*100+count['stwo']*10
    return score


def game_win(list):
    """
    胜利条件判断
    """
    for m in range(COLUMN):
        for n in range(ROW):
            # 一列
            if n <= ROW - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (
                    m, n + 3) in list and (m, n + 4) in list:
                return True
            # 一行
            elif m <= ROW - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (
                    m + 3, n) in list and (m + 4, n) in list:
                return True
            # 左上右下
            elif m <= ROW - 4 and n < ROW - 4 and (m, n) in list and (m + 1, n + 1) in list and (
                    m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                return True
            # 左下右上
            elif m <= ROW - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (
                    m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                return True
    return False

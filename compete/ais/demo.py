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
# 不同情况的分数，用于评估局势（有较大缺陷）
shape_score = [(50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (5000, (0, 1, 1, 1, 0)),
               (5000, (0, 1, 0, 1, 1, 0)),
               (5000, (0, 1, 1, 0, 1, 0)),
               (5000, (1, 1, 1, 0, 1)),
               (5000, (1, 1, 0, 1, 1)),
               (5000, (1, 0, 1, 1, 1)),
               (5000, (1, 1, 1, 1, 0)),
               (5000, (0, 1, 1, 1, 1)),
               (50000, (0, 1, 1, 1, 1, 0)),
               (99999999, (1, 1, 1, 1, 1))]


def ai(listAI, listHuman, list_all):
    """
    AI计算落子位置
    """
    # 先手第一步下在最中间
    if len(listHuman) == 0:
        next_point[0] = 7
        next_point[1] = 7
    else:
        # 将listAI与listHuman顺序加入到listAIAndHuman
        for i in range(len(listAI)):
            listAIAndHuman.append(listAI[i])
        for i in range(len(listHuman)):
            listAIAndHuman.append(listHuman[i])
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
    if x >= 0 and x < 15 and y >= 0 and y < 15:
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
        myScore = 0
        # 对该点四个方向进行评估（复用了打分函数，不过可能需要修改，当前效率还很低）
        myScore += cal_score(node[0], node[1], 0, 1, enemyList, myList, [])
        myScore += cal_score(node[0], node[1], 1, 0, enemyList, myList, [])
        myScore += cal_score(node[0], node[1], 1, 1, enemyList, myList, [])
        myScore += cal_score(node[0], node[1], -1, 1, enemyList, myList, [])
        tmp[node] = myScore
    return [item[0] for item in sorted(tmp.items(), key=lambda item: item[1], reverse=True)]


def evaluation(is_ai, listAI, listHuman):
    """
    评估函数（效率较低）
    """
    if is_ai:
        my_list = listAI
        enemy_list = listHuman
    else:
        my_list = listHuman
        enemy_list = listAI
    # score_all_arr的格式[(score,shape)]
    score_all_arr = []  # 得分形状的位置 用于计算如果有相交 得分翻倍
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score(m, n, 0, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 0, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, 1, 1, enemy_list, my_list, score_all_arr)
        my_score += cal_score(m, n, -1, 1, enemy_list, my_list, score_all_arr)
    # 算敌人的得分， 并减去
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score(m, n, 0, 1, my_list,
                                 enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 0, my_list,
                                 enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, 1, 1, my_list,
                                 enemy_list, score_all_arr_enemy)
        enemy_score += cal_score(m, n, -1, 1, my_list,
                                 enemy_list, score_all_arr_enemy)

    total_score = my_score - enemy_score * 1
    return total_score


def cal_score(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr):
    """
    每个方向上的分值计算
    :param m:
    :param n:
    :param x_decrict:
    :param y_derice:
    :param enemy_list:
    :param my_list:
    :param score_all_arr:
    :return:
    """
    add_score = 0  # 加分项
    # 在一个方向上， 只取最大的得分项
    max_score_shape = (0, None)

    # 如果此方向上，该点已经有得分形状，不重复计算
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    # 在落子点 左右方向上循环查找得分形状
    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                pos.append(1)
            else:
                pos.append(0)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                # 找到最高评分，将分数与各点坐标存储到max_score_shape中
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0 + offset) * x_decrict, n + (0 + offset) * y_derice),
                                               (m + (1 + offset) * x_decrict,
                                                n + (1 + offset) * y_derice),
                                               (m + (2 + offset) * x_decrict,
                                                n + (2 + offset) * y_derice),
                                               (m + (3 + offset) * x_decrict,
                                                n + (3 + offset) * y_derice),
                                               (m + (4 + offset) * x_decrict, n + (4 + offset) * y_derice)),
                                       (x_decrict, y_derice))

    # 计算两个形状相交， 如两个3活 相交， 得分增加 一个子的除外
    if max_score_shape[1] is not None:
        # 如果找到了得分形状
        for item in score_all_arr:
            # 遍历所有点的最高分
            for pt1 in item[1]:
                # 遍历所有点最高分数组中的所有点
                for pt2 in max_score_shape[1]:
                    # 遍历当前最高分数组中的所有点
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        # 如果有相同点并且分数大于10（大于10是没用的约束条件），额外加双倍的分数
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)
    # 返回额外加分与最高评分的和
    return add_score + max_score_shape[0]


def game_win(list):
    """
    胜利条件判断
    """
    for m in range(COLUMN):
        for n in range(ROW):
            # 一列
            if n < ROW - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (
                    m, n + 3) in list and (m, n + 4) in list:
                return True
            # 一行
            elif m < ROW - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (
                    m + 3, n) in list and (m + 4, n) in list:
                return True
            # 左上右下
            elif m < ROW - 4 and n < ROW - 4 and (m, n) in list and (m + 1, n + 1) in list and (
                    m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                return True
            # 左下右上
            elif m < ROW - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (
                    m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                return True
    return False

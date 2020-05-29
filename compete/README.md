# 五子棋AI的实现

1.  实现过程

    基本思路为使用极大极小值算法，综合alpha-beta剪枝，局势评估函数应用了单点评估，最后返回的分数为：
    $$
    score=myScore-enemyScore\times defend
    $$
    其中myScore为我方所有点分数总和，enemyScore为敌方所有点分数总和，defend为防守系数（该系数越大，五子棋越偏向于防守），单点评估函数取该点“米”字方向的连续九个点，接着对这九个点进行连五、活四、冲四、活三、眠三、活二，眠二的判断，最后将四个方向分数累加。

    剪枝过程同样应用了单点评估函数对所有的可能点进行了排序，增加剪枝效率。（可能点指的是所有在当前已经使用过的点旁边的点。）

2.  测试过程

    参照`runChess.py`实现了相应的函数，但调试起来颇为不便，于是外接了一个图形界面（使用`tkinter`）对函数进行调用。

    经过测试，该AI在大多数情况下能够战胜我，且无论先手后手均能战胜`demo`：

    ![战胜我.jpg](https://allwens-work.oss-cn-beijing.aliyuncs.com/bed/image-20200529132906764.png)

    ---

    ![image-20200529133920408](https://allwens-work.oss-cn-beijing.aliyuncs.com/bed/image-20200529133920408.png)

    ![image-20200529134500709](https://allwens-work.oss-cn-beijing.aliyuncs.com/bed/image-20200529134500709.png)

3.  核心算法

    核心算法为带有alpha-beta剪枝的负极大值算法：

    ```python
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
    ```

4.  重要优化

    +   使用启发式搜索（即先对所有可能点进行排序，增加剪枝效率）：

        ```python
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
            # 通过value对key进行排序
            return [item[0] for item in sorted(tmp.items(), key=lambda item: item[1], reverse=True)]
        ```

    +   换用了更加有效的单点评估函数：

        ```python
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
        ```

        

    
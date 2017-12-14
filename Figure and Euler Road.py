# -*- coding:utf-8 -*-

# 南邮离散数学第四次实验
# 图的随机生成及欧拉(回)路的确定

# 整体思路，先生成无向图的邻接矩阵，然后判断这个图是否是连通图，如果是连通图，
# 再通过计算每个结点的度，判定是否是欧拉图

import numpy as np  # 引入numpy库进行矩阵运算


def create_adjacency_matrix(num):  # 创建无向图的邻接矩阵
    x = np.random.randint(0, 2, (num, num))  # 生成一个全随机的邻接矩阵，但是并非无向图，因为该矩阵并不对称
    for i in range(num):  # 将对角置为0
        x[i][i] = 0
    x = np.matrix(x)  # 将该数组转换为矩阵

    for i in range(num):
        for j in range(i + 1, num):
            x[j, i] = x[i, j]  # 将不对称的矩阵按照上三角部分，变为对称矩阵

    print('随机生成的无向图的邻接矩阵为：\n', x)
    return x


def dfs(matrix_, visited, start):  # 深度优先遍历
    visited[start] = True  # 将当前点置为True
    size = int(matrix_.size**(1/2))
    for i in [x for x in range(size) if x != start]:  # 遍历除输入点外的其他点，看是否能够到达
        if matrix_[start, i] and not visited[i]:  # 如果能到达，并且标记数组为False，则进行递归调用
            dfs(matrix_, visited, start=i)


def is_connectivity_diagram(matrix_, start=0):
    """
    判断是否是连通图
    """
    lists = [False for _ in range(num)]  # 生成一个全False列表，作为局部变量，传入给dfs函数
    dfs(matrix_, lists, start)
    return all(lists)  # 如果lists中所有元素为True，证明该图是个连通图


def get_deg(matrix_):  # 获取每个点的度
    lists = []  # 临时列表用来存储
    size = int(matrix_.size**(1/2))
    for i in range(size):
        temp_num = 0
        for j in range(size):
            if i != j and matrix_[i, j]:  # 遍历矩阵该行
                temp_num += 1
        lists.append(temp_num)  # 将该点的度加入到列表中
    return lists


def is_euler(deg):
    """
    判断是否是欧拉图或者半欧拉图
    """
    result = len([x for x in deg if x % 2])  # 获取奇数度结点
    if result == 0:  # 如果只有零个奇数度结点
        return True, True  # 则为欧拉图
    elif result == 2:  # 如果有两个奇数度节点
        return True, False  # 则为半欧拉图
    else:
        return (False,)  # 其他均为非欧拉图，为了程序的通用性，这里返回tuple


if __name__ == '__main__':
    num = int(input('输入n作为矩阵的维度:'))
    matrix_ = create_adjacency_matrix(num)
    is_con = is_connectivity_diagram(matrix_)
    if is_con:
        print('该图是连通图...')
    else:
        print('该图不是连通图...')
    deg = get_deg(matrix_)
    print('该图中每个节点的度：\n', deg)
    result = is_euler(deg)
    if result[0] and is_con:
        if result[1]:
            print('该图是欧拉图...')
        else:
            print('该图是半欧拉图...')
    else:
        print('该图不是欧拉图...')

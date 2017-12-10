# 南邮离散数学第三次实验
# 偏序关系中盖住关系的求取以及格论中有补格的判定

# 设定二元关系为整除
# 根据格的定义：如果A是一个偏序集，其中任意两个元素都有最小上界和最大下界，则称A为格。
# 在整除中，任意两个元素的最小公倍数就是这两个元素的最小上界
# 任意两个元素的最大公约数就是这两个元素的最大下界

import numpy as np


def gcd(a, b):
    """
    辗转相除法求最大公约数
    """
    if a < b:
        a, b = b, a
    while b:
        a, b = b, a % b
    return a


def icm(a, b):
    """
    利用gcd求最小公倍数
    """
    return a * b / gcd(a, b)


def get_poset(x):
    """
    使用列表推导式将所有因子计算出，最后使用列表加法将本身加入，
    得到偏序集元素。
    """
    return [i for i in range(1, x//2 + 1) if not x % i] + [x]


def get_relation_matrix(matrix_, poset):
    """
    计算获取关系矩阵
    """
    size = int(matrix_.size**(1/2))  # 获取矩阵的大小
    for x in range(size):
        for y in range(size):
            if not poset[y] % poset[x]:  # 通过判断是否能整除，计算关系矩阵
                matrix_[x, y] = 1
    return matrix_


def get_cover(matrix_, poset):
    """
    计算盖住集（与计算传递性类似）
    """
    lists = []  # 创建空列表存储盖住关系
    # print(matrix_)
    size = int(matrix_.size ** (1 / 2))  # 获取矩阵的大小
    for x in range(size):  # 先将对角线上的元素全部置为零，不然的话，整个矩阵处理过后，全为零
        matrix_[x, x] = 0
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if matrix_[x, y] and matrix_[y, z]:  # 根据条件将不满足盖住条件的矩阵元素置零
                    matrix_[x, z] = 0
    for x in range(size):
        for y in range(size):
            if matrix_[x, y]:
                lists.append([poset[x], poset[y]])  # 将矩阵元素对应的值加入组成序偶加入到盖住集中
    return lists  # 返回盖住集


def is_complemented_lattice(poset):
    """
    判断是否是有补格
    """
    for x in range(len(poset)):
        sign = False  # 初始化标志量
        for y in range(len(poset)):
            if x == y:
                continue
            if gcd(poset[x], poset[y]) == 1 and icm(poset[x], poset[y]) == poset[-1]:
                # 如果该两个元素的最大下界为1，最小上界为最大值，则满足有补格的定义
                sign = True  # 修改标志量
                break
        if not sign:  # 如果某次循环结束之后，标志量为False，证明该两个元素不满足有补格定义
            return False
    return True


def main():
    print('----- 请输入用来计算偏序集的number -----')
    poset = get_poset(int(input()))
    max_length = len(poset)
    a = np.zeros((max_length, max_length), dtype=np.int16)
    a = np.matrix(a)
    matrix_demo = get_relation_matrix(a, poset)
    cover_set = get_cover(matrix_demo, poset)
    print('盖住关系:\n', cover_set)
    print('是否是有补格: {}'.format(is_complemented_lattice(poset)))


if __name__ == '__main__':
    main()

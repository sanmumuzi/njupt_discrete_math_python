import numpy as np  # 使用numpy库进行矩阵运算

lists = []  # 建立list存储序偶

while True:
    temp_str = input().strip()  # 防止输入时过多地输入空格
    if not temp_str:  # 当输入空行时退出
        break
    lists.append([int(temp_str[0]), int(temp_str[-1])])  # 将序偶插入列表

# print(lists)
max_num = max((max(x) for x in lists))  # 得出输入中
a = np.zeros((max_num, max_num), dtype=np.int16)  # 通过输入的最大值，创建全零数组，使用int16类型
for x in lists:
    a[x[0]-1, x[1]-1] = 1  # 通过遍历序偶，将对应位置置为1

x = np.matrix(a)  # 将数组转换为矩阵
# print(x)


def is_reflexivity(matrix_):  # 判断是否具有自反性
    return matrix_.diagonal().all()  # 判断关系矩阵的对角线元素是否全部为1


def is_anti_reflexive(matrix_):  # 判断是否具有反自反性
    return not matrix_.diagonal().any()  # 判断关系矩阵的对角线元素是否全不为1


def is_symmetry(matrix_):  # 判断是否具有对称性
    matrix_ = matrix_.getA()  # 将matrix类型转换为ndarray类型
    for row in range(max_num):
        for col in range(row+1, max_num):
            if matrix_[row][col] != matrix_[col][row]:  # 判断矩阵是否是沿主对角线对称
                return False
    return True


def is_antisymmetry(matrix_):  # 判断是否具有反对称性
    matrix_ = matrix_.getA()  # 将matrix类型转换为ndarray类型
    for row in range(max_num):
        for col in range(row + 1, max_num):
            if matrix_[row][col] == matrix_[col][row] == 1:  # 判断矩阵是否是沿主对角线对称
                return False
    return True


def is_transitivity(matrix_):  # 判断是否具有传递性
    temp = warshall(matrix_)  # 使用Warshall算法
    matrix_ = matrix_.getA()
    for row in range(max_num):
        for col in range(max_num):
            if temp[row][col] != matrix_[row][col]:
                return False
    return True


def warshall(matrix_):  # 使用Warshall算法
    temp = matrix_.getA().copy()  # 请注意：这里必须使用copy创建副本，否则将修改原数据，这样无论如何，都满足传递性。
    for i in range(max_num):
        for j in range(max_num):
            if temp[j][i] == 1:  # 对所有j如果A[j，i]＝1，则对k＝1，2，…，n，A[j，k]＝A[j，k]∨A[i，k]
                for k in range(max_num):
                    if any([temp[j][k], temp[i][k]]):  # 取并集
                        temp[j][k] = 1
    return temp  # t(R)的关系矩阵


print('具有自反性：', is_reflexivity(x))
print('具有反自反性：', is_anti_reflexive(x))
print('具有对称性：', is_symmetry(x))
print('具有反对称性：', is_antisymmetry(x))
print('具有传递性：', is_transitivity(x))

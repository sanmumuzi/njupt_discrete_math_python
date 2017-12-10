# 南邮离散数学第一次实验
# 使用真值表法求主析取范式和主合取范式
# 未使用任何库

combine, extract, negate = '∧∨┓'  # 定义变量代表合取、析取、取反
condition, double_condition = '→↔'  # 定义条件、双条件
priority = {  # 定义优先级
    extract: 3,
    combine: 4,
    negate: 5,
    condition: 2,
    double_condition: 1
}  # 优先级字典

enter_expression = input('请输入表达式：')  # 得到中缀表达式
temp_demo = '(P∧Q)∨(┓P∧R)∨(Q∧R)'  # 三个测试用例
temp_demo1 = '(┓P∨┓Q)→(P↔┓Q)'
temp_demo2 = 'P→((P→Q)∧┓(┓Q∨┓P))'


def get_suffix_expression(enter_expression):  # 该函数用于获取后缀表达式
    finally_str = ''  # 后缀表达式
    operator_stack = []  # 操作符栈
    temporary_expression_stack = []  # 临时表达式栈

    for temp_char in enter_expression:  # 遍历输入的中缀表达式
        if temp_char not in priority and temp_char not in {'(', ')'}:  # 判断是否为操作数
            temporary_expression_stack.append(temp_char)
        elif temp_char in priority.keys():  # 判断是否为操作符
            temp_sign = True  # 操作标志量
            while temp_sign:  # 如果未操作完成，将会一直循环，并不会报错，最坏的情况下即为操作符栈为空。
                if len(operator_stack) == 0 or operator_stack[-1] == '(':  # 如果操作符栈为空或者栈顶操作符为左括号
                    operator_stack.append(temp_char)  # 直接压入
                    temp_sign = False
                elif priority[temp_char] > priority[operator_stack[-1]]:  # 判断当前操作符优先级是否大于操作符栈中的栈顶元素
                    operator_stack.append(temp_char)  # 直接压入
                    temp_sign = False
                else:
                    temporary_expression_stack.append(operator_stack.pop())  # 将操作符栈顶的元素出栈，压入临时表达式栈
        elif temp_char in {'(', ')'}:  # 判断是否为左右括号
            if temp_char == '(':
                operator_stack.append(temp_char)  # 左括号直接压入操作符栈
            else:
                while operator_stack[-1] != '(':  # 直到遇到左括号，不停止
                    temporary_expression_stack.append(operator_stack.pop())  # 将操作符栈顶的元素出栈，压入临时表达式栈
                operator_stack.pop()  # 删除左括号

    while len(operator_stack):  # 将操作符栈中的剩余元素全部压入临时表达式栈
        temporary_expression_stack.append(operator_stack.pop())

    for _ in temporary_expression_stack:  # 将列表转换为字符串
        finally_str += _
    return finally_str  # 返回后缀表达式


s = get_suffix_expression(enter_expression)
print('后缀表达式：', s)  # 打印后缀表达式

arg_lists = []  # 存储该表达式的操作数
for x in s:
    if x not in {'(', ')'} and x not in priority and x not in arg_lists:
        arg_lists.append(x)

print('该表达式拥有{}个变量....'.format(len(arg_lists)))

test_dict = {}  # 该字典存储key(变量)和value(真假)
globals_zhuxiqu = []  # 最终的主析取范式
globals_zhuhequ = []  # 最终的主合取范式


def out_lists(test_dict):  # 计算每一种情况下，最终表达式的真假。
    temp_out_lists = []
    for x in s:
        if x not in {'(', ')'} and x not in priority:  # 判断x是否为操作数
            temp_out_lists.append(bool(test_dict[x]))  # 将变量的真假压入
        if x in priority:  # 如果为操作数，按操作数种类分情况
            if x == extract:  # 如果操作是析取
                x = temp_out_lists.pop()  # 栈顶出栈
                y = temp_out_lists.pop()  # 次顶出栈
                temp_out_lists.append(any([x, y]))  # 析取，将结果入栈
            elif x == combine:  # 如果操作是合取
                x = temp_out_lists.pop()  # 栈顶出栈
                y = temp_out_lists.pop()  # 次顶出栈
                temp_out_lists.append(all([x, y]))  # 合取，将结果入栈
            elif x == negate:  # 如果操作是取反
                x = temp_out_lists.pop()  # 栈顶出栈
                temp_out_lists.append(not x)  # 取反，将结果入栈
            elif x == condition:  # 如果操作是条件
                x = temp_out_lists.pop()  # 栈顶出栈
                y = temp_out_lists.pop()  # 次顶出栈
                if y and x:
                    temp_out_lists.append(True)
                if not y:
                    temp_out_lists.append(True)
                else:
                    temp_out_lists.append(False)
            elif x == double_condition:  # 如果操作是双条件
                x = temp_out_lists.pop()  # 栈顶出栈
                y = temp_out_lists.pop()  # 次顶出栈
                if x == y:
                    temp_out_lists.append(True)
                else:
                    temp_out_lists.append(False)
    return temp_out_lists[0]  # 最后列表中只剩一项，即为当前情况下表达式最终结果


for x in range(pow(2, len(arg_lists))):  # n的变量会有2的n次方的情况
    str_item = '{0:0' + str(len(arg_lists)) + 'b}'  # 将0到2的n次方-1转化为与参数个数长度相同的位数的二进制
    k = str_item.format(x)  # 格式化字符串
    # print(k, arg_lists)
    for i, j in enumerate(arg_lists):  # 枚举
        test_dict[j] = int(k[i])  # 为变量设置默认值
    end = out_lists(test_dict)  # test_dict 为表示该种情况的字典，获取该种情况下的表达式结果
    str_hequ = ''  # 主合取范式的每一小项
    str_xiqu = ''  # 主析取范式的每一小项
    for i, j in test_dict.items():  # 遍历字典，打印真值表
        print(i, j, end=' ')  # i对应变量，j对应真假
        if end:  # 如果最终结果为真
            if j:  # 构成主析取范式
                str_xiqu += i + combine
            else:
                str_xiqu += negate + i + combine  # 如果为假，进行取反
        else:
            if not j:  # 构成主合取范式
                str_hequ += i + extract
            else:
                str_hequ += negate + i + extract  # 如果为假进行取反
    print('表达式最终结果：', end)  # 打印出最终结果
    if end:
        str_xiqu = str_xiqu[:-1]  # 将字符串最后多出来的操作符去掉
        str_xiqu = '(' + str_xiqu + ')'  # 左右加上括号
        globals_zhuxiqu.append(str_xiqu)
    else:
        str_hequ = str_hequ[:-1]
        str_hequ = '(' + str_hequ + ')'
        globals_zhuhequ.append(str_hequ)

str_zhuhequ = combine.join(globals_zhuhequ)  # 将主合取范式用操作符连接
str_zhuxiqu = extract.join(globals_zhuxiqu)

print('主合取范式为：', str_zhuhequ)  # 打印最终结果
print('主析取范式为：', str_zhuxiqu)

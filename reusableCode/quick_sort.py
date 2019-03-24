# 快速排序
# 分而治之


def quick_sort(alist):
    '''
    1. 随机定一个元素为基准
    2. 比基准小的置于基准左侧，大的置于右侧
    3. 递归调用此过程
    :param alist:
    :return:
    '''
    if len(alist) <= 1:
        return alist
    else:
        pivot = alist[0]
        return quick_sort([i for i in alist[1:] if i < pivot]) + \
            [pivot] + \
            quick_sort([i for i in alist[1:] if i > pivot])


if __name__ == '__main__':
    print(quick_sort([6, 5, 3, 1, 8, 7, 2, 4]))
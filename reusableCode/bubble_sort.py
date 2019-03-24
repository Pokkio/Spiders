# 冒泡排序
# 复杂度 O(n^2)
'''
比较相邻的元素。如果第一个比第二个大，就交换他们两个。
对第0个到第n-1个数据做同样的工作。这时，最大的数就“浮”到了数组最后的位置上。
针对所有的元素重复以上的步骤，除了最后一个。
持续每次对越来越少的元素重复上面的步骤，直到没有任何一对数字需要比较。
'''


def bubble_sort(array):
    n = len(array)
    for i in range(n):
        # 优化：某一趟遍历如果没有数据交换，则说明已经排好序了，因此不用再进行迭代了。
        # 用一个标记记录这个状态即可。
        flag = 1
        for j in range(1, n - i):
            if array[j - 1] > array[j]:  # 如果前者大于后者
                array[j], array[j - 1] = array[j - 1], array[j]  # 两者交换位置
                flag = 0
        if flag:
            break
    return array


if __name__ == '__main__':
    print(bubble_sort([1, 2, 3, 5, 4]))
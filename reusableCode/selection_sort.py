# 选择排序
# 复杂度 O(n^2)
'''
在未排序序列中找到最小（大）元素，存放到排序序列的起始位置。
再从剩余未排序元素中继续寻找最小（大）元素，然后放到未排序序列的开头。
以此类推，直到所有元素均排序完毕。
'''


def select_sort(array):
    n = len(array)
    for i in range(n):
        min_index = i  # 最小值下标
        for j in range(i + 1, n):
            if array[j] < array[min_index]:
                min_index = j  # 找到当前最小值
                # array[min_index], array[i] = array[i], array[min_index]
        array[min_index], array[i] = array[i], array[min_index]
    return array


if __name__ == '__main__':
    print(select_sort([0, 3, 2, 1, 5, 4, 8]))
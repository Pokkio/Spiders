# 插入排序


def insert_sort(array):
    n = len(array)
    for i in range(1, n):
        if array[i] < array[i - 1]:
            temp = array[i]
            index = i  # 插入下标
            for j in range(i-1, 0, -1):  # 从后往前遍历
                if array[j] > temp:
                    array[j+1] = array[j]
                    index = j
                else:
                    break
            array[index] = temp
    return array


if __name__ == '__main__':
    print(insert_sort([0, 3, 2, 4, 8, 6, 5]))
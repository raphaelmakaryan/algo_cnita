from itertools import permutations


def tri_insertion(array):
    n = len(array)
    for i in range(1, n):
        j = i
        while j > 0 and array[j - 1] > array[j]:
            array[j] = array[j - 1]
            j = j - 1
            array[j] = array[i]
    print(array)


def tri_selection_sort(array):
    for i in range(1, len(array)):
        min = i
        for j in range(min + 1, len(array)):
            if array[j] < array[min]:
                min = j
            if min is not i:
                array_tempo = array[i]
                array[i] = array[min]
                array[min] = array_tempo
    print(array)


def buble_sort(array):
    passage = 0
    permutation = True
    while permutation:
        permutation = False
        for i in range(0, (len(array) - 1) - passage):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = \
                    array[i + 1], array[i]
                permutation = True
        passage = passage + 1
    print(array)

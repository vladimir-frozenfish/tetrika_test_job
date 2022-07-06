"""
Дан массив чисел, состоящий из некоторого количества
подряд идущих единиц, за которыми следует какое-то количество
подряд идущих нулей: 111111111111111111111111100000000.
Найти индекс первого нуля (то есть найти такое место,
где заканчиваются единицы, и начинаются нули)
"""
import time
from bisect import bisect_right


def task(array: list) -> int:
    try:
        return array.index(0)
    except ValueError:
        return -1


def task_bisect(array: list) -> int:
    len_arr = len(array)
    if len_arr == 0:
        return -1

    index_0 = len_arr - bisect_right(array[::-1], 0)
    return -1 if len_arr == index_0 else index_0


if __name__ == '__main__':
    print(task([0, 0, 0, 0, 0, 0, 0]))
    print(task([1, 1, 1, 1, 0, 0, 0]))
    print(task([1, 1, 1, 1, 1, 1, 1]))
    print(task([]))

    print()

    print(task_bisect([0, 0, 0, 0, 0, 0, 0]))
    print(task_bisect([1, 1, 1, 1, 0, 0, 0]))
    print(task_bisect([1, 1, 1, 1, 1, 1, 1]))
    print(task_bisect([]))

    print()

    # поиск в большом массиве
    array = [1] * 100000000 + [0] * 10

    start_func = time.perf_counter()
    print(task(array))
    stop_func = time.perf_counter()
    print(f'Время выполнения поиска index: {round(stop_func - start_func, 5)}')

    start_func = time.perf_counter()
    print(task_bisect(array))
    stop_func = time.perf_counter()
    print(f'Время выполнения поиска bisect: {round(stop_func - start_func, 5)}')
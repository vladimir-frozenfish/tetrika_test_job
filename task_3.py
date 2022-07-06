"""
Было бы просто, если мы исходим из того, что интервалы отсортированы, правильно
указаны началои конец и не пересекаются сами с собой

Но ученик, во втором тесте сумел раздвоится и у него есть пересекающиеся интервалы,
поэтому необходима функция, которая возвращает интервалы без пересечений
для этого написана функция intersect_interval, которая объединяет пересекающиеся интервалы
ученика. Если с учителем будет такая же проблема, то такую функцию стоит применить и к интервалам
учителя, прежде чем их сравнивать с интервалом урока

функция intersect_interval была мною написана ранее для решения задачи подсчета суммы интервалов
на сайте - www.codewars.com
"""


def intersect_interval(intervals):
    """функция получает интервалы в виде списка и возвращает
    список непересекающихся интервалов из первоначального списка"""
    result_list = [-1, -1]

    """цикл по всем интервалам"""
    for i in range(0, len(intervals), 2):
        left_barier = 0
        right_barier = 0

        left_valeu = intervals[i]
        right_value = intervals[i+1]

        """первая проверка - если первое значение интервала меньше первого 
        значение в результирующем списке, то оно сразу добавляется в список 
        вначале дважы, для сохранения парности интервалов"""
        if left_valeu < result_list[0]:
            result_list.insert(0, left_valeu)
            result_list.insert(0, left_valeu)
        else:
            """цикл по результирующему списку интервалов.
            за раз берется один интервал (два числа)
            чикл с конца
            проверка для левого значени интервала"""
            for i in range(len(result_list)-1, -1, -2):
                """если проверяемое значение больше последнего
                значения, то
                он добавляется в результирующий лист дважды, для сохранения
                парности интервалов"""
                if left_valeu > result_list[i]:
                    result_list.insert(i+1, left_valeu)
                    result_list.insert(i+1, left_valeu)
                    left_barier = i+1
                    break
                elif left_valeu <= result_list[i] and left_valeu >= result_list[i-1]:
                    left_barier = i-1
                    break

        """цикл по результирующему списку интервалов.
        за раз берется один интервал (два числа)
        цикл с конца проверка для правого значени интервала"""
        for i in range(len(result_list) - 1, -1, -2):

            """если проверяемое значение больше последнего
            значения, то он добавляется в результирующий лист"""
            if right_value > result_list[i]:
                result_list.insert(i + 1, right_value)
                right_barier = i + 1
                break
            elif right_value <= result_list[i] and right_value >= result_list[i - 1]:
                right_barier = i
                break

        """удаление лишних интервалов в границах барьеров"""
        del result_list[left_barier+1 : right_barier]

    return result_list[2:]


def appearance(intervals):
    """функция получает словарь с интервалами урока,
    интервалами учителя и ученика
    вовзращает общее время нахождения учителя и ученика на уроке"""
    lesson_start = intervals['lesson'][0]
    lesson_end = intervals['lesson'][1]

    """отсекаем интервалы учителя, которые не входят во время урока"""
    intervals_tutor = []
    for i in range(0, len(intervals['tutor']), 2):
        tutor_start = intervals['tutor'][i]
        tutor_end = intervals['tutor'][i+1]

        # если интервал учителя полностью не входит в урок,
        # то пропускаем этот интервал
        if tutor_end < lesson_start or tutor_start > lesson_end:
            continue

        if tutor_start < lesson_start:
            tutor_start = lesson_start
        if tutor_end > lesson_end:
            tutor_end = lesson_end

        intervals_tutor.append((tutor_start, tutor_end))

    """получение интервалов ученика без пересечений"""
    intervals_pupil = intersect_interval(intervals['pupil'])

    intervals_common = []
    """цикл интервалов ученика"""
    for i in range(0, len(intervals_pupil), 2):
        pupil_start = intervals_pupil[i]
        pupil_end = intervals_pupil[i+1]

        """сравниваем текущий интервал ученика 
        с каждым интервалом учителя"""
        for tutor_start, tutor_end in intervals_tutor:
            if pupil_end < tutor_start:
                break
            if pupil_start > tutor_end:
                continue

            pupil_start_temp = pupil_start
            pupil_end_temp = pupil_end
            if pupil_start < tutor_start:
                pupil_start_temp = tutor_start
            if pupil_end > tutor_end:
                pupil_end_temp = tutor_end

            intervals_common.append((pupil_start_temp, pupil_end_temp))

    """подсчет времени общих интервалов"""
    total_time = 0
    for common_start, common_end in intervals_common:
        total_time += (common_end - common_start)

    return total_time

tests = [
    {'data': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'data': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'data': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        print(test_answer == test['answer'])

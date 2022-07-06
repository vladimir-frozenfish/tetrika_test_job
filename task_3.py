"""
исходим из того, что интервалы отсортированы, правильно
указаны началои конец и не пересекаются сами с собой

но ученик, во втором тесте сумел раздвоится и у него есть пересекающиеся интервалы,
поэтому необходима функция, которая возвращает интервалы без пересечений
"""

def intersect_interval(intervals):
    """функция возвращает интервалы без пересчений"""
    intervals_not_inttersect = []

    for i in range(0, len(intervals), 2):
        current_start = intervals[i]
        current_end = intervals[i+1]

        count = 0
        # for start, end in intervals_not_inttersect:
        while count < len(intervals_not_inttersect):
            start = intervals_not_inttersect[count][0]
            end = intervals_not_inttersect[count][1]

            # если текущий интервал входит полностью в сравниваемый,
            # то этот интервал не вносится, цикл прерывается
            if current_start >= start and current_end <= end:
                break
            # если текущий интервал находится слева от сравниваемого,
            # то он добавляется перед сравниваемым и цикл прерывается
            if current_end <= start:
                intervals_not_inttersect.insert(count, (current_start, current_end))
                break

            count += 1


def appearance(intervals):
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

    intervals_pupil = intersect_interval(intervals['pupil'])

    intervals_common = []
    """цикл интервалов ученика"""
    for i in range(0, len(intervals['pupil']), 2):
        pupil_start = intervals['pupil'][i]
        pupil_end = intervals['pupil'][i+1]

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

    print(intervals_common)
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
   # for i, test in enumerate(tests):
   #     test_answer = appearance(test['data'])
   #     assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        print(test_answer == test['answer'])



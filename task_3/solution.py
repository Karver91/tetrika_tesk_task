def appearance(intervals: dict[str, list[int]]) -> int:
    def get_intervals(lst: list[int]) -> list[tuple]:
        result = []
        for i in range(0, len(lst), 2):
            result.append((lst[i], lst[i + 1]))
        return result

    def merge_intervals(intervals):
        """Объединяем пересекающиеся друг с другом интервалы"""
        if not intervals:
            return []
        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        merged = [sorted_intervals[0]]
        for current in sorted_intervals[1:]:
            a_start, a_end = merged[-1]
            b_start, b_end = current
            # Ищем пересечения интервалов
            if b_start < a_end and b_end > a_start:
                # Склеиваем пересекающиеся интервалы
                merged[-1] = (a_start, max(a_end, b_end))
            else:
                merged.append(current)
        return merged

    def interval_intersection(interval_1, interval_2):
        result = []
        for i in interval_1:
            a_start, a_end = i

            for j in interval_2:
                b_start, b_end = j

                if b_start < a_end and b_end > a_start:
                    result.append((max(a_start, b_start), min(a_end, b_end)))

        return result

    # Извлекаем интервалы из словаря
    lesson = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']

    # Интервалы урока
    lesson_interval = get_intervals(lesson)

    # Интервалы ученика
    pupil_intervals = get_intervals(pupil)
    merged_pupil = merge_intervals(pupil_intervals)

    # Интервалы учителя
    tutor_intervals = get_intervals(tutor)
    merged_tutor = merge_intervals(tutor_intervals)

    # Находим пересечение урока и ученика
    pupil_lesson = interval_intersection(lesson_interval, merged_pupil)
    # Находим пересечение с учителем
    total_intersection = interval_intersection(pupil_lesson, merged_tutor)

    # Суммируем общее время
    return sum(end - start for start, end in total_intersection)


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

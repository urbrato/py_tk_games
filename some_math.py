def clamp(value: int, min: int, max: int) -> int :
    '''
    Ограничение диапазона значения.

    Возвращает исходное значение, если оно лежит в заданном диапазоне.
    Иначе возвращает соответствующую границу диапазона

    :param value: исходное значение
    :type value: int
    :param min: минимальное допустимое значение
    :type min: int
    :param max: максимальное допустимое значение
    :type max: int
    
    :rtype: int
    :return возвращает исходное значение, если оно лежит в заданном диапазоне, 
    иначе возвращает соответствующую границу диапазона
    '''
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value
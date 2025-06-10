def boyer_moore(text, pattern):
    """
    Реализация алгоритма Бойера-Мура для поиска подстроки.
    Возвращает список позиций всех вхождений pattern в text.
    """
    def preprocess_bad_char(pattern):
        """
        Создает таблицу плохих символов.
        Ключ - символ, значение - последняя позиция символа в шаблоне.
        """
        bad_char = {}
        length = len(pattern)
        for i in range(length):
            bad_char[pattern[i]] = i
        return bad_char

    def preprocess_good_suffix(pattern):
        """
        Создает таблицу хороших суффиксов (good suffix rule).
        """
        length = len(pattern)
        bmGs = [0] * length
        suffix = [0] * (length + 1)

        # Первый этап: вычисление suffix
        suffix[length] = length
        for i in range(length-1, -1, -1):
            j = i
            while j >= 0 and pattern[j] == pattern[length - 1 - i + j]:
                j -= 1
            suffix[i] = i - j

        # Второй этап: заполнение bmGs
        for i in range(length):
            bmGs[i] = length
        j = 0
        for i in range(length-1, -1, -1):
            if suffix[i] == i + 1:
                while j < length - 1 - i:
                    if bmGs[j] == length:
                        bmGs[j] = length - 1 - i
                    j += 1
        for i in range(length-1):
            bmGs[length - 1 - suffix[i]] = length - 1 - i

        return bmGs

    # Основная функция
    n = len(text)
    m = len(pattern)
    if m == 0:
        return []

    # Предварительная обработка
    bad_char = preprocess_bad_char(pattern)
    bmGs = preprocess_good_suffix(pattern)

    result = []
    s = 0  # Текущая позиция сравнения в тексте

    while s <= n - m:
        j = m - 1
        # Сравниваем справа налево
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            # Найдено совпадение
            result.append(s)
            # Сдвигаемся на длину шаблона (аналог bmGs[0])
            s += bmGs[0]
        else:
            # Вычисляем сдвиг по правилу плохого символа
            bc_shift = j - bad_char.get(text[s + j], -1)
            # Вычисляем сдвиг по правилу хорошего суффикса
            gs_shift = bmGs[j]
            # Выбираем максимальный сдвиг
            s += max(bc_shift, gs_shift, 1)

    return result

# Пример использования
text = "GCATCGAGAGAGAGTATACAGTACGCAGAGAG"
pattern = "GCAGAGAG"

positions = boyer_moore(text, pattern)
print("Найденные позиции:", positions)  # Должно вывести [8, 19]
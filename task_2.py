"""
Получить с русской википедии список всех животных (https://inlnk.ru/jElywR) и
вывести количество животных на каждую букву алфавита.
Результат должен получиться в следующем виде:
А: 642
Б: 412
В:....
"""

import requests
import string

from collections import defaultdict


def animal_to_table(html_text):
    """функция получает html-код страницы и возвращает
    данные животных в виде
    <li><a href=.... title=...>...</a></li>"""
    animal_table = str()

    start_find = 0
    while True:
        start_index_category_group = html_text.find('</h3>\n<ul><li><a href="/wiki/', start_find)
        if start_index_category_group == -1:
            break
        end_index_category_group = html_text.find('</ul></div>', start_index_category_group)

        animal_table += html_text[start_index_category_group + 10:end_index_category_group]

        start_find = end_index_category_group

    return animal_table


def animal_to_list(animal_table):
    """функция получает данные о животных в виде
    <li><a href=.... title=...>...</a></li>
    и взвращает список наименований животных"""
    animal = []
    start_find = 0

    while True:
        index_start = animal_table.find('title=', start_find)
        if index_start == -1:
            break
        index_end = animal_table.find('">', index_start)
        animal.append(animal_table[index_start + 7:index_end])

        start_find = index_end

    return animal


def main():
    animal_dict = defaultdict(int)                                          # словарь для занесения количества животных по первой букве

    with open('animals.txt', 'w'):                                           # создание пустого файла или очистка от предыдущих данных если он был создан
        pass

    url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'    # первоначальный url на стартовую страницу

    russian = True
    while russian:
        response = requests.get(url)
        response.encoding = 'utf-8'
        html_text = response.text

        animal_table = animal_to_table(html_text)                           # из HTML-текста страницы получение списка животных <li><a > ... </li>
        animals = animal_to_list(animal_table)                              # получение списка животных

        next_page_animal = animals.pop()                                    # последнее животное в списке для генерации следующей страницы
        url = f'https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&pagefrom={next_page_animal}#mw-pages'

        """запись в файл полученных животных
        занесение значений по первой букве животного в словарь"""
        with open('animals.txt', 'a') as file:
            for animal in animals:
                if animal == 'Aaaaba':                                      # цикл идет до первого животного на латинице
                    russian = False
                    break
                if animal[0] in string.ascii_uppercase:                     # если в перечне животных на русском попадется животное на латинице, то его пропускаем
                    continue
                file.writelines(animal + '\n')
                animal_dict[animal[0]] += 1

    """запись словаря с количеством животных на определенные 
    буквы в файл и вывод в консоль"""
    with open('animals_dict.txt', 'w') as file:
        for key, value in sorted(list(animal_dict.items())):
            file.writelines(f'{key}: {value}\n')
            print(f'{key}: {value}')


if __name__ == '__main__':
    main()

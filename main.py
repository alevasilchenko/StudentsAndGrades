import sqlite3
import os
import random

NEW_RANDOM_BASE = False  # признак необходимости рандомного создания базы данных
# При установке значения True ранее созданная база данных будет удалена и перезаписана заново случайным контентом.
# Прилагаемая база данных также была создана с использованием рандомных функций.
# При формировании случайного контента учитываются налагаемые ТЗ ограничения.

DB_NAME = 'students.db'  # имя файла базы данных

UNIVERSITY_NAME = 'Urban University'  # наименование учебного заведения

SUBJECTS_LIST = ['iOS', 'Frontend', 'Android', 'UI/UX', 'QA', 'Python', 'Analyst']  # перечень специализаций


class University:  # созданный, согласно ТЗ, класс

    def __init__(self, name: str):

        self.name = name

    def add_student(self, name: str, age: int):  # метод добавления студента
        cursor.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
        db.commit()

    def add_grade(self, student_id: int, subject: str, grade: float):  # метод добавления оценки
        cursor.execute("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)", (student_id, subject, grade))
        db.commit()

    def get_students(self, subject=None):  # метод для возврата списка студентов
        sql = (f"SELECT students.name, students.age, grades.subject, grades.grade "
               f"FROM students, grades WHERE (students.id = grades.student_id)")
        if subject:
            sql += f" AND (grades.subject = '{subject}')"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results


print()

if NEW_RANDOM_BASE:  # если установлен признак формирования нового рандомного контента базы данных

    try:
        os.remove(DB_NAME)  # удаляем файл БД при его наличии
    except FileNotFoundError:
        pass

db = sqlite3.connect(DB_NAME)
cursor = db.cursor()

urban_university = University(UNIVERSITY_NAME)

if NEW_RANDOM_BASE:  # если установлен признак формирования нового рандомного контента базы данных

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name STRING NOT NULL,
    age INTEGER NOT NULL)
    ''')  # создаём таблицу студентов

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    student_id INTEGER NOT NULL,
    subject STRING NOT NULL,
    grade FLOAT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id))
    ''')  # создаём таблицу оценок

    all_students = []
    number_of_students = random.randint(4, 10)  # количество студентов от 4 до 10

    for i in range(number_of_students):

        one_student = {}

        student_name = ''
        length_of_student_name = random.randint(3, 10)  # длина имени студента от 3 до 10

        for _ in range(length_of_student_name):
            student_name += chr(random.randint(ord('a'), ord('z')))  # формируем рандомное имя студента

        one_student['name'] = student_name.capitalize()  # делаем имя с заглавной буквы

        student_age = random.randint(18, 50)  # возраст студента от 18 до 50
        one_student['age'] = student_age

        student_subjects = set()
        number_of_subjects = random.randint(2, 7)  # количество изучаемых студентом специализаций от 2 до 7

        for j in range(number_of_subjects):
            while len(student_subjects) <= j:
                student_subjects.add(random.choice(SUBJECTS_LIST))  # рандомный выбор специализаций

        academic_performance = []  # список зачётов добавляемого студента

        for student_subject in student_subjects:
            subject_grade = round(random.randint(10, 50) / 10, 1)  # диапазон оценок от 1.0 до 5.0
            academic_performance.append((student_subject, subject_grade))

        one_student['grade'] = academic_performance

        all_students.append(one_student)

    st_id = 0
    for student in all_students:
        st_id += 1
        urban_university.add_student(student['name'], student['age'])  # добавляем запись в таблицу студентов
        for subj in student['grade']:
            urban_university.add_grade(st_id, subj[0], subj[1])  # добавляем запись в таблицу оценок


for subject_name in SUBJECTS_LIST:  # пробегаем по всему перечню специализаций
    subject_result = urban_university.get_students(subject_name)  # получаем список студентов по заданной специализации
    print(f'{subject_name.upper():8}: ', end='')
    if subject_result:
        print(subject_result)
    else:
        print(f'По направлению {subject_name} обучающиеся не найдены... (((')

incorrect_subject_name = 'C++'
print(f'\nНа некорректный запрос ({incorrect_subject_name}) '
      f'будет выведен пустой список: {urban_university.get_students(incorrect_subject_name)}')

print(f'\nНа пустой запрос будет выведена вся база данных: {urban_university.get_students()}')

db.close()

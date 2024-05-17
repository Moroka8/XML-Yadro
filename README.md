# Общая информация
Базовая станция – сложный аппаратно-программная система по приему и передаче
радиосигналов, способная работать со множеством мобильных устройств одновременно.
Аппаратная часть состоит в том числе из антенны и одного или нескольких радиомодулей,
связанных между собой физически. Программная часть состоит из большого количества
сервисов, работающих вместе на одном «железе», при этом каждый из них отвечает за
конкретный функционал. Координирующим узлом в программной части выступает система
управления базовой станцией.

Важной частью системы управления базовой станции является информационная модель, которая
представляет собой формальную UML-диаграмму с описанием иерархической структуры классов
и их атрибутов. Данная модель разрабатывается в специализированных программах, которые
предоставляют удобный интерфейс для одновременной совместной работы над моделями,
хранение их в БД, разграничение доступа. В процессе эволюции системы в модель регулярно
вносятся изменения (появляются новые классы, изменяются атрибуты и т.д.).
Модель в виде рисунка понятна и привычна для человека, но для компьютерной обработки
удобнее другой формат, более приближенный к машинному, поэтому модель может быть
переведена в XML-файл, однозначно соответствующий UML-диаграмме.
Полученный XML проверяется на непротиворечивость и отсутствие ошибок (при разработке всегда
может сыграть человеческий фактор) – этот процесс мы называем валидацией. Если ошибок нет,
запускается генерация определенных частей исходного кода – артефактов – по сути,
интерфейсов для программ всех компонент базовой станции (к ним относятся файлы
конфигурации, YANG-файлы, исходники на С++ и Go, Proto-файлы и т.д.). Одновременный переход
всех компонент на новую версию артефактов позволяет избежать ошибок несовместимости
версий и является одной из первоочередных задач системы управления базовой станцией.

# Информационная модель
Для тестового задания предлагается некоторая упрощенная модель, из которой убраны лишние
связи и атрибуты, но тем не менее она использует те же принципы, что и основная ее версия:
XML-файл модели состоит из двух логических частей – описание классов и описание связей между
ними. Каждый класс содержит описание атрибутов (если они есть), каждый атрибут имеет тип.
Связи между классами – агрегации. Для каждой из них указано два имени – target (класс,
включающий в себя другой класс) и source (класс, включенный в другой класс). Также в
отношениях агрегации указаны мощности (multiplicity) – может быть как одно число, так и
диапазон [min..max].\
Файл: impulse_test_input.xml
# Задание
Требуется написать программу на Python, которая на основе входного XML-файла
(impulse_test_input.xml) генерирует следующие виды выходных файлов (артефактов):
1. Файл config.xml представляет собой пример внутренней конфигурации базовой станции,
соответствующий представленной модели.
2. Файл meta.json содержит мета-информацию о классах и их атрибутах. Фронтенд
использует данный файл для корректного отображения дерева объектов в интерфейсе
пользователя (UI).

Требования к решению
1. Исполнение программы должно осуществляться запуском файла main.py без параметров
из корня архива. Сгенерированные файлы при этом должны сохраняться в папке out.
2. Скрипты корректно работают на Python версии 3.11
3. Можно использовать библиотеки, входящие в стандартный комплект поставки Python

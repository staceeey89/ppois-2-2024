# Лабораторная работа №1

<span style="font-size: 25px;">__Цель:__</span><br>
1. Изучить основные возможности языка Python для разработки программных систем с интерфейсом командной строки (CLI)<br>
2. Разработать программную систему на языке Python согласно описанию предметной области
<hr>

<span style="font-size: 25px;">__Задача:__</span><br>
<u>__Разработать программную систему на языке Python. Модель проведения научной конференции 31___</u>

Предметная область: организация и проведение научных мероприятий.

Важные сущности: оргкомитет, ученые, докладчики, темы докладов, программный комитет, конференц-зал.

Операции: операция приема заявок на участие, операция выбора тем и докладчиков, операция организации программы, операция проведения регистрации участников, операция подготовки и проведения конференции.
<hr>

<span style="font-size: 25px;">__Описание работы программы:__</span><br>

```
Классы:

* Класс Conference
* Класс CommitteeMember
* Класс ConferenceHall
* Класс Presentation
* Класс Scientist
* Класс Speaker
* Класс Person
* Класс OrganizingCommittee
```
<hr>

<span style="font-size: 25px;">__Класс Conference:__</span><br>
### Методы
- \_\_init__(self, name, location, start_date, end_date, max_participants, application_deadline, coffee_breaks, lunch_break)

Создает конференцию с указанным названием, местом события, началом и концом события, максимальным числом участников, сроком подачи заявок, перерывами на кофе и обед

- accept_application(self, participant)

Принимает заявку на участие (принята/уже была зарегистрирована/срок подачи заявок истек/не такого участника)

- add_speaker(self, speaker)

Добавляет выступающего на конференцию

- select_presentation(self, presentation)

Выбирается тема для докладчика (смотрится его опыт и квалификация)

- organize_program(self)

Организация расписания конференции (я взяла начало с 9 утраи потом каждый час выступление, также учитываются перерывы на обед и кофе)

- register_participant(self, participant)

Регистрация участников (до максимального количества)

- prepare_conference(self), conduct_conference(self)

Подготовка и проведение конференции (проверяется все ли участники зарегистрированы и всё ли оборудование работает(check_projector(self), check_microphones(self), check_sound_system(self)))

Если докладчик не готов:

- handle_unprepared_speaker(self, speaker)

Перенос презентации при условии, что 1) есть свободное другое время (can_reschedule_presentation(self, speaker)) или 2) возможна замена докладчика (can_replace_speaker(self, speaker))

- cancel_presentation(self,speaker)

Отмена презентации

- generate_icalendar(self)

Создание календаря, где отслеживаются все события конференции

- collect_feedback(self)

Получение обратного фидбека от просмотра выступления (пятибалльная шкала оценивания + комментарий)

- notify_participants(self, message)

Уведомление участников о событии конференции
<hr>

<span style="font-size: 25px;">__Класс ComitteeMember (Person):__</span><br>
### Методы
- \_\_init__(self, name, affiliation)

Создает члена комитета с именем и принадлежностью

- assign_task(self, task, priority="средний", deadline=None)

Получение задачи с приоритетом

- complete_task(self, task)

Выполнение задачи (или ошибка, если она не найдена)

- review_paper(self, paper)

Рецензирование статьи

- vote(self, decision)

Голосование

- organize_meeting(self, meeting_time)

Организация встречи

- send_reminder(self, reminder)

Отправка напоминаний

- delegate_task(self, task, member)

Делегирование задачи

- generate_task_report(self)

Сводка выполненных и невыполненных задач для члена комитета
<hr>

<span style="font-size: 25px;">__Класс ConferenceHall:__</span><br>
### Методы
- \_\_init__(self, name, capacity)

Создает зал для конференций с названием и вместимостью

- add_booking(self, booking)

Добавляет бронь

- cancel_booking(self, booking)

Отменяет бронь (с ошибкой, если бронь не найдена)
<hr>

<span style="font-size: 25px;">__Класс Presentation:__</span><br>
### Методы
- \_\_init__(self, title, speaker: Speaker, topic)

Создает презентацию доклада с названием, темой и самим докладчиком

- add_slide(self, slide_content)

Добавляет слайд в презентацию
<hr>

<span style="font-size: 25px;">__Класс Scientist (Person):__</span><br>
### Методы
- \_\_init__(self, name, affiliation, field_of_study)

Создает учёного с именем, членством, областью исследований

- publish_research(self, research)

Публикация исследования

- write_grant_proposal(self, grant_info)

Написание предложения по гранту

- attend_conference(self, conference_info)

Возможность послать ученого на конференцию

- collaborate_with(self, other_scientist)

Возможность добавления сотрудничества двух ученых

- track_achievements(self, achievement)

Выводит достижения ученого

- subscribe_to_journals(self, journal_list)

Подписка на научные журналы
<hr>

<span style="font-size: 25px;">__Класс Speaker (Person):__</span><br>
### Методы
- \_\_init__(self, name, affiliation, presentation_topic, experience_level, preferred_time)

Создает докладчика с именем, членством, темой доклада, уровнем квалификации и предпочтительным временем выступления

- average_rating(self)

Считает средний рейтинг докладчика

- display_info(self)

Выводит всю информацию о докладчике
<hr>

<span style="font-size: 25px;">__Класс Person:__</span><br>
### Методы
- \_\_init__(self, name, affiliation)

Создает человека с именем и членством
<hr>

<span style="font-size: 25px;">__Класс OrganizingCommittee:__</span><br>
### Методы
- \_\_init__(self, chairperson, members)

Создает оргкомитет c председателем и членами

- add_member(self, new_member)

Добавляет члена в оргкомитет

- remove_member(self, member_to_remove)

Удаляет члена из оргкомитета
<hr>

<span style="font-size: 25px;">__Покрытие моего кода unit-тестами:__</span><br>

<div style="text-align: center;">
    <img src="" style="height: 400px">
</div>
<hr>

<span style="font-size: 25px;">__Вывод:__</span><br>
В результате выполнения лабораторной работы были изучены ключевые возможности языка Python для создания программ с интерфейсом командной строки.В рамках лабораторной работы была успешно разработана программная система на Python, моделирующая функциональность научной конференции. Это позволило понять применимость Python для разработки эффективных и удобных CLI-приложений и создать работоспособную систему для управления задачами и данными в рамках модели научной конференции.
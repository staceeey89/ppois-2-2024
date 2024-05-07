# Лабораторная работа №3

<span style="font-size: 25px;">__Цель:__</span><br>
• Изучить событийно-ориентированное программирование с использованием библиотеки на языке Python (рекомендуется библиотека pygame)


<span style="font-size: 25px;">__Вариант 4. Arkanoid__</span><br>

<hr>

Моя программа содержит в себе:
• 10 игровых уровней на выбор;
• 5 модификаций для разнообарзия игры;

Структура каждого уровня, а также основные настройки игры прописаны в конфигах.

<div style="text-align: center;">
    <img src="https://sun9-20.userapi.com/impg/1xHt67wdQ081H67YXBxfLynq9-GOeXYyFaF-2g/eYRM8jdy8ao.jpg?size=270x184&quality=96&sign=ef9b4726c72c43402163f52cd0593c2f&type=album" style="height: 200px;">
</div>

```
В моей лабораторной использованы .yaml файлы для хранения конфигов.

Пеимущества:

• Читаемость: По сравнению с другими форматами, такими как JSON, YAML имеет удобную для человека структуру, что облегчает чтение и понимание данных.
• Вложенность: YAML поддерживает вложенные структуры данных, позволяя организовать информацию в логичной иерархии.
• Гибкость: YAML допускает комментарии, что позволяет добавлять примечания и пояснения к данным. Он также позволяет использовать произвольные ключи и позволяет значениям иметь несколько строк.
• Компактность: YAML, как правило, более компактен, чем XML или JSON, что позволяет сэкономить место при хранении данных.
• Легкость в использовании: YAML имеет простой синтаксис, что облегчает создание и редактирование файлов.
• Расширяемость: YAML позволяет определять пользовательские теги и схемы для поддержки специализированных типов данных.
```

_Пример описания уровня в конфигах:_
<div style="text-align: center;">
    <img src="https://sun9-28.userapi.com/impg/sm_uVsoiK0Fn04jRCDGFh2K-MymB_vJwcS9Tjg/eIaSzKVr4Ec.jpg?size=362x900&quality=96&sign=f3691ceb9c1bf56f87a29add196112d3&type=album" style="height: 500px;">
</div>
<hr>

Код программы содержит классы для структуризации игры и корректного создания парадигмы Событийно-ориентированного программирования.
<div style="text-align: center;">
    <img src="https://sun9-63.userapi.com/impg/NqYW5wbrBRZOggO80YFV23wtpN0eeNJukfIKMA/itsQhZSAs6w.jpg?size=250x519&quality=96&sign=926ebda96a6da6758521b37fdfe46a22&type=album" style="height: 300px;">
</div>
<hr>

Основной экран игры содержит __4 кнопки__:
- _Играть_ - позволяет выбрать уровень и начать игру;
- _Рекорды_ - позволяет посмотреть текущие рекорды людей;
- _Справка_ - позволяет посмотреть правила игры;
- _Выход_ - оканчивает игру.

Кнопка "Играть" вызывает экран выбора уровня.
<div style="text-align: center;">
    <img src="https://sun9-49.userapi.com/impg/NVrDIiiZCcb0oY4fus9AjhFlGxwnZfd-vv8ung/9ltwB2TjzfI.jpg?size=1498x977&quality=96&sign=8c99d304306fc0208c672f99ec0dd487&type=album" style="height: 300px;">
</div>

При нажатии на уровень запускается класс __Arkanoid_display__, который подключает классы для корректного внешнего вида уровня, а также корректного поведения игры

_Пример уровня игры:_
<div style="text-align: center;">
    <img src="https://sun9-11.userapi.com/impg/Bi2VldJk8B7SkS96CM3mOjWrpO7i2322MNeSPQ/RiJ5opZjhxg.jpg?size=1496x982&quality=96&sign=78dbe79323b5d61b09c82f72a39192ce&type=album" style="height: 300px;">
</div>

<hr>

Игра также имеет музыкальное сопровожджение:
- Музыка основного фона
- Музыка на кааждом уровне
Также игра имеет звуки:
- Звук удара мяча
- Звук получения модификации
- Звук победы
- Звук поражения

В игре присутствуют __5 модифиакторов:__
- _Модификатор увеличения платформы_
- _Модификатор уменьшения платформы_
- _Модификатор замедления времени_
- _Модификатор добавления нового шара_
- _Модификатор создания блокирующей платформы_

```
Данные модификаторы также прописаны в конфигах
```
<div style="text-align: center;">
    <img src="https://sun9-40.userapi.com/impg/pyR2qCOemYl3HcPtH25_H079rqTGX0meKa_ukg/Q0VNCPxCMGE.jpg?size=1026x315&quality=96&sign=3c908618f4f80dbe4a8066b1bb4a751e&type=album" style="height: 200px;">
</div>

Моя игра включает в себя __3 вида кубиков:__
- Зеленые - ломаются с одного удара
- Синие - ломаются с двух ударов
- Красные - ломаются с трех ударов

```
При попаданиии, например, в синий кубик, он переходит из списка синих в список зеленый с изменением цвета. После повторного попадания он пропадает из зеленого списка и удаляется полностью
```
<hr>

В игре существует __5 модификаторов:__
- _"Удлиннитель"_
<div style="text-align: center;">
    <img src="https://sun9-7.userapi.com/impg/gPh4N8lrk68VoBxd1fqA0a7Cb1idSXMjW8pNHA/k2FZvvNfiKA.jpg?size=59x28&quality=96&sign=3d11702ff65f4642efc1a7962434122e&type=album" style="height: 100px;">
</div>

```
Увеличивает длину платформы
```

<hr>

- _"Укоротитель"_
<div style="text-align: center;">
    <img src="https://sun9-39.userapi.com/impg/YpAI4VDHm63ZGMF33wZRty_cmEXc6SvPj7RLGA/gjWP1CSHhFI.jpg?size=59x28&quality=96&sign=696a7416b00328700973118977553eb6&type=album" style="height: 100px;">
</div>

```
Уменьшает длину платформы
```

<hr>

- _"Замедлитель"_
<div style="text-align: center;">
    <img src="https://sun9-19.userapi.com/impg/SHoNBcOwZ1d7Vc79ccoNXchTSWNSgrrHED6zJg/prLEGrnZY-w.jpg?size=59x28&quality=96&sign=4ad628f7484dcc014b71f1916e757d85&type=album" style="height: 100px;">
</div>

```
Замедляет fps, чтобы снизить скорость игры
```

<hr>

- _"Дубликат"_
<div style="text-align: center;">
    <img src="https://sun9-30.userapi.com/impg/6gLu192Zjxjx-N8SKAxkAbLjg7M3i6ZAVG-N7w/WAWdYoZV9I8.jpg?size=59x28&quality=96&sign=55df753163cf61490ae40323807def62&type=album" style="height: 100px;">
</div>

```
Создает новый шарик на карте
```
<hr>

- _"Блокировщик"_
<div style="text-align: center;">
    <img src="https://sun9-76.userapi.com/impg/yeC-9lkhFXcIIt-vBcyvMGE3S0Aw_D9mNAIyNA/k0JTAUmnPdM.jpg?size=59x28&quality=96&sign=21f3d6088f54fce7484d84b0b59dfc07&type=album" style="height: 100px;">
</div>

```
Создает платформу, которая блокирует низ карты. После одного удара платформа пропадает
```
<hr>

• При проигрыше раунда вы можете вернуться на главное меню.
• При победе в уровне, если ваше время меньше, чем время игрока в первой строчке, то вас попросит вписать свой ник, чтобы сохраниться в рекордах (пустым ник быть не может)

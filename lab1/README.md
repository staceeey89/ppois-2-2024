# Лабораторная работа 1
## Вариант 65: Модель государства

Предметная область: политика, управление, законодательство.

Важные сущности: правительство, законы, граждане, инфраструктура, экономика, внешние отношения.

Операции: операция законодательного процесса, операция налогообложения, операция обеспечения безопасности, операция социальной поддержки, операция управления экономикой.

## Классы
### State
#### Свойства
- `government: Government`
- `economy: Economy`
- `external_politics: ExternalPolitics`
- `population: Population`
- `legislation: Legislation`
### Government
#### Свойства
- `head: Citizen`
#### Методы
- `change_head(Citizen)`
  
  Изменяет главу правительства
- `provide_security(Citizen) -> str`

  Обеспечивает безопастность
- `provide_social_support(Citizen) -> str`

  Обеспечивает социальную поддержку
### Economy
#### Свойства
- `treasury: int`
#### Методы
- `collect_taxes(Citizen)`

  Собирает налог с гражданина
- `enhance_infrastructure()`

  Улучшает инфраструктуру
### ExternalPolitics
#### Свойства
- `relations: list[ExternalRelation]`
#### Методы
- `add_external_relation(ExternalRelation)`

  Добавляет внешнее отношение
- `get_external_relation(State) -> ExternalRelation`

  Возвращает внешнее отношение с государством state
- `remove_external_relation(ExternalRelation)`

  Удаляет внешнее отношение
### Legislation
#### Свойства
- `laws: list[Law]`
#### Методы
- `add_law(Law)`

  Добавляет закон
- `get_law(str) -> Law`

  Возвращает закон c заголовком str
- `remove_law(Law)`

  Удаляет закон
### Population
#### Свойства
- `citizens: list[Citizen]`
#### Методы
- `add_citizen(Citizen)`

  Добавляет гражданина
- `get_citizen(str) -> Citizen`

  Возвращает гражданина c именение str
- `remove_citizen(Citizen)`

  Удаляет гражданина
### Interpreter
#### Методы
- `interpret(Input): Command`

  Интерпретирует Input и возвращает команду
### Command
#### Свойства
- `name: str`
#### Методы
- `execute -> str`

  Исполняет командe, возвращает сообщение об выполнении команды
- `can_execute -> bool`

  Проверяет на возможность выполнения команды
### Inputer
#### Методы
- `get_input -> Input`

  Забирает и парсит ввод, возвращает input
### Terminal
#### Методы
- `do_iteration -> str`

  Берёт ввод, передает интерпретатору и выполняет команду
  

## Модель отеля

### Описание

#### Цель:  

- Изучить основные возможности языка Python для разработки программных систем с интерфейсом командной строки (CLI) 
- Разработать программную систему на языке Python согласно описанию предметной области

#### Задачи: 

- Разработать программную систему по предметной области: гостиничный бизнес и обслуживание гостей. 
- Реализовать операции:
    1. Операция бронирования номера
    2. Операция регистрации гостей
    3. Операция предоставления дополнительных услуг
    4. Операция обслуживания в ресторане
    5. Операция выселения и оплаты

- Реализовать ключевые сущности:
    1. Номер
    2. Гость
    3. Персонал
    4. Бронирование
    5. Ресепшен
    6. Сервисные услуги


### Релизация

 - ##### Номер

Cущность номера в отеле состоит из следующих полей:

- Номер комнаты
- Тип номера (ECONOMY, STANDARD, LUXURY)
- Статус номера (EMPTY, OCCUPIED)

##### Фрагмент кода:
```python
class HotelRoom:
  def __init__(self, number: str, type_of_room: RoomType, status: RoomStatus):
    self.__number = number
    self.__type_of_room = type_of_room
    self.__status = status
```

- ##### Гость

Гость наследуется от класса Person, его поля:

 - Имя
 - Возраст
 - Номер пасспорта

##### Фрагмент кода:
```python
class Person:
  def __init__(self, name: str, age: int, passport_id: str):
    self.__name = name
    self.__age = age
    self.__passport_id = passport_id


class Visitor(Person):
  def __init__(self, name: str, age: int, passport_id: str):
    super().__init__(name, age, passport_id)
```

- ##### Персонал

Персонал так же как и гость наследуется от класса Person, расширяя его свойства полем "status"

Свойства класса Worker:

 - Имя
 - Возраст
 - Номер пасспорта
 - Статус (RESTING, WORKING)

##### Фрагмент кода:
```python
class Worker(Person):
  def __init__(self, name: str, age: int, passport_id: str, status: WorkerStatus):
    super().__init__(name, age, passport_id)
    self.__status = status
```

- ##### Бронирование

Сущность бронирования включает в себя следующие поля:

 - Гость
 - Номер в отеле
 - Дата начала бронирования
 - Дата конца бронирования
 - Статус бронирования (RENTING, FINISHED)

##### Фрагмент кода:
```python
class Booking:
  def __init__(self, visitor: Visitor, room: HotelRoom,
               start_date: datetime, finish_date: datetime, status: BookStatus):
    self.__visitor = visitor
    self.__room = room
    self.__start_date = start_date
    self.__finish_date = finish_date
    self.__status = status
```

- ##### Ресепшен

Ресепшен включает в себя следующие поля:

 - Список гостей
 - Список текущих броней
 - Список невыполненных услуг
 - Список номеров


##### Фрагмент кода:
```python
class Reception:
  def __init__(self):
    self.__visitors: list[Visitor] = []
    self.__bookings: list[Booking] = []
    self.__services: list[Service] = []
    self.__rooms: list[HotelRoom] = []
```

В классе ресепшен осуществляется реализация основной логики системы.
Ресепшен реализует следующие операции:

__Операция бронирования номера__

```python
def book(self, visitor_passport_id, room_number: str, start_date: datetime, finish_date: datetime) -> Booking:
  visitor = self.find_visitor(visitor_passport_id)
  if not visitor:
    raise VisitorNotFoundException(visitor_passport_id)
  room = self.find_room(room_number)
  if not room:
    self.__visitors.remove(visitor)
    raise BookingException("No such room")
  if room not in self.find_available_rooms():
    self.__visitors.remove(visitor)
    raise BookingException("Room is not available now")
  room.status = RoomStatus.occupied
  booking = Booking(visitor, room, start_date, finish_date, BookStatus.renting)
  self.__bookings.append(booking)
  return booking
```

__Операция регистрации гостей__

```python
def registrate_visitor(self, visitor: Visitor) -> bool:
  if visitor not in self.__visitors:
    self.__visitors.append(visitor)
    return True
  return False


def find_visitor(self, visitor_passport_id: str) -> Visitor | None:
  for visitor in self.__visitors:
    if visitor.passport_id == visitor_passport_id:
      return visitor
  return None
```

__Операция предоставления дополнительных услуг__

```python
def ask_for_service(self, visitor_passport_id: str, service_type: ServiceType, worker: Worker):
  visitor = self.find_visitor(visitor_passport_id)
  if not visitor:
    raise VisitorNotFoundException(visitor_passport_id)
  self.__services.append(Service(visitor, service_type, worker))
  worker.status = WorkerStatus.working


def finish_service(self, worker_passport_id) -> Service | None:
  for service in self.__services:
    if service.worker.passport_id == worker_passport_id:
      self.__services.remove(service)
      return service
  return None
```

__Операция обслуживания в ресторане__

```python
def ask_for_restaurant_service(self, visitor_passport_id: str, worker: Worker, dishes: list[Dishes]):
  visitor = self.find_visitor(visitor_passport_id)
  if not visitor:
    raise VisitorNotFoundException(visitor_passport_id)
  self.__services.append(RestaurantService(visitor, ServiceType.restaurant, worker, dishes))
  worker.status = WorkerStatus.working
```

__Операция выселения и оплаты__

```python
def finish_booking(self, visitor_passport_id: str) -> Booking:
  visitor = self.find_visitor(visitor_passport_id)
  if not visitor:
    raise VisitorNotFoundException(visitor_passport_id)
  booking = self.find_booking_by_visitor_passport_id(visitor_passport_id)
  if not booking:
    raise BookingException("Booking not found")
  booking.room.status = RoomStatus.empty
  booking.status = BookStatus.finished
  self.__visitors.remove(visitor)
  self.__bookings.remove(booking)
  return booking
```

- ##### Отель

Отель включает в себя следующие поля:

 - Ресепшен
 - Список работников отеля


##### Фрагмент кода:
```python
class Hotel:
  __PAYMENT_PER_DAY = 100

  def __init__(self):
    self.__reception = Reception()
    self.__workers: list[Worker] = []
```

В основном методы класса "Отель" валидируют информацию необходимую для корректного выполнения методов класса "Ресепшен".
А также отлавливают и реагируют на исключения пробрасываемые методами класса "Ресепшен"

__Пример__

Метод выполняющий операцию выселения и оплаты

```python
def pay_off(self, visitor_passport_id: str) -> bool:
  try:
    booking: Booking = self.__reception.finish_booking(visitor_passport_id)
    days: int = (booking.finish_date - booking.start_date).days
    print(f"""Payment for {days} days is {days * Hotel.__PAYMENT_PER_DAY * booking.room.type.value[1]}""")
    return True
  except BookingException as e:
    print(e)
    return False
  except VisitorNotFoundException as e:
    print(e)
    return False
```

- #### Исключения

```python
class BookingException(Exception):
  def __init__(self, message: str):
    self.__message = message

  def __str__(self) -> str:
    return self.__message


class VisitorNotFoundException(Exception):
  def __init__(self, visitor_passport_id: str):
    self.__message = f"Visitor with passport id '{visitor_passport_id}' doesn't exist"

  def __str__(self) -> str:
    return self.__message
```

### Диаграмма классов

![UML Class diagram](/resources/class_diagram.png)

### Диаграмма состояний

![UML State diagram](/resources/state_diagram.png)


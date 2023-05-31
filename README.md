# practic-bot-itmo
### Запуск:
Для запуска бота нужно сначала загрузить библиотеки командой "pip install (название библиотеки)" <br>
<a>Список библиотек: aiogram, httplib2, google-api-python-client, oauth2client</a>

### Как привязать таблицу для вопросов и регистрации:
Для привязки таблицы нужно получить json-ключ(руководство по получению ключа: https://habr.com/ru/articles/483302/), после его получения нужно добавить его в проект и переименовать на my.json <br>

Далее нужно заменить sheetId в файле interactor.py на id таблицы, которую мы хотим использовать(id таблицы можно найти в ссылке на таблицу # id таблицы https://docs.google.com/spreadsheets/d/xxxxx/edit#gid=0, xxxxx это id).
Теперь таблица создана, не надо переименовывать листы (ЛИСТ 1 для сохранения зарегеистрованных пользователей, ЛИСТ 2 для популярных вопросов), как выглядит таблица можно посмотреть по ссылке https://docs.google.com/spreadsheets/d/1LudWwZpHk3wrqkZkX103py7NVM7oUA6Yctjrnog63UA/edit#gid=38077366

### Как добавить команды на стартовую клаивиатуру:
В файле main.py в функции getStartKeyboard, нужно добавить в стартовую клавиатуру KeyboardButton('/навзание_команды'), на подобии '/register' и '/popular_questions'
```python
def getStartKeyboard() -> ReplyKeyboardMarkup:
    start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    start_kb.add(KeyboardButton('/register')).add(KeyboardButton('/popular_questions'))
    return start_kb
```
И далее реализовать обработчик команды. Обработчик команды обозначается @dp.message_handler(commands=['навзание_команды']), и под ним реализовать функцию обработчика
Выглядит это примерно так
```python
@dp.message_handler(commands=['name_command'])
async def name_command(message: types.Message) -> None:
  # Код для команды
```

Также, чтобы избежать ошибок при регистрации, требуется внести в каждую функцию, которая имеет в обработчике:
```python
@dp.message_handler(lambda message: message.text in ['/start', '/register', '/popular_questions'], ...)
```
внести название команды, чтобы избежать возможности багов в регистрации.

### Как изменить регистрацию:
Чтобы добавить пункт в регистрацию для начала нужно добавить стейт для регистрации в файле main.py
```python
class Profile(StatesGroup):
    name = State()
    group = State()
    educational_practice = State()
    educational_practice_2 = State()
    industrial_practice = State()
    other_industrial_practice = State()
    work_industrial_practice = State()
    other_industrial_practice_fileName = State()
    undergraduate_practice = State()
```
Добавить нужно в формате: name_state = State() и расположить в какой момент нам нужно будет вызвать этот пункт.

Далее нужно реализовать обработчик пункта, он должен выглядеть примерно так для ввода строки:
```python
@dp.message_handler(state=Profile.name_state)
async def register_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name_state'] = message.text

    await message.reply('Вопрос для след пункта регистрации')
    await Profile.next()
```

Также нужно добавить функцию проверки корректности ввода, она будет выглядеть примерно так
```python
@dp.message_handler(lambda message: message.text in ['/start', '/register', '/popular_questions'], state=Profile.name_state)
async def invalid_register_name_state(message: types.Message) -> None:
    await message.answer('Название ошибки')
```
В lambda message: мы пишем условия проверки, в функции вверху проверяется сообщение отправленное боту, если оно есть в массиве, то функция проверки сообщает, что ввод был некорректен

### Как добавить вопросы:
Вопросы нужно просто добавить в используемой таблице на ЛИСТ2 по форме показанной тут https://docs.google.com/spreadsheets/d/1LudWwZpHk3wrqkZkX103py7NVM7oUA6Yctjrnog63UA/edit#gid=38077366

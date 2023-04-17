from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from interactor import loadDataToSheet, getQuestions

# Токен для бота
TOKEN_API = "6111052062:AAEoMe16L3yIWiHDQBG6I2BD6pLZWmrg1IU"

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

questions = []


# Стейты для регистрации
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


# Стартовая клавиатура
def getStartKeyboard() -> ReplyKeyboardMarkup:
    start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    start_kb.add(KeyboardButton('/register')).add(KeyboardButton('/popular_questions'))
    return start_kb


@dp.message_handler(commands=['start'])
async def start(message: types.Message) -> None:
    await bot.send_message(message.from_user.id, text='Привет, я бот практики. Я занимаюсь сбором информации и также '
                                                      'отвечаю на'
                                                      'популярные вопросы.', reply_markup=getStartKeyboard())


# Начало регистрации
@dp.message_handler(commands=['register'])
async def register(message: types.Message) -> None:
    await message.reply("Сейчас тебя зарегестрируем.\nТвое ФИО")
    await Profile.name.set()


@dp.message_handler(state=Profile.name)
async def register_name(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply('Номер твоей группы')
    await Profile.next()


@dp.message_handler(state=Profile.group)
async def register_group(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['group'] = message.text

    await message.reply('<b>Учебаная практика</b>\n1.Итмо\n2.Сторонняя организация (договор на практику '
                        'и заявка)\n3.По месту работы (приношу копию трудового и '
                        'заявление)\n4.Перезачёт стажировки'
                        '\n<b>отправьте номер выбранного варианта</b>', parse_mode='html')
    await Profile.next()


@dp.message_handler(state=Profile.educational_practice)
async def register_educational_practice(message: types.Message, state: FSMContext) -> None:
    if message.text == '1':
        dataMessage = 'Итмо'
    elif message.text == '2':
        dataMessage = 'Сторонняя организация (договор на практику и заявка)'
    elif message.text == '3':
        dataMessage = 'По месту работы (приношу копию трудового и заявление)'
    elif message.text == '4':
        dataMessage = 'Перезачёт стажировки'
    else:
        dataMessage = 'not'

    async with state.proxy() as data:
        data['educational_practice'] = dataMessage

    await message.reply('<b>Учебная практика:</b>\n1) если ИТМО: ФИО полностью и должность руководителя '
                        'практики, подразделение\n2) если сторонняя организация или по месту работы: '
                        'полное или краткое наименование организации, ИНН, ФИО руководителя практики '
                        'полностью, контактный номер телефона, корпоративный адрес', parse_mode='html')
    await Profile.next()


@dp.message_handler(state=Profile.educational_practice_2)
async def register_educational_practice_2(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['educational_practice_2'] = message.text

    await message.reply('<b>Производственная практика:</b>\n1) если ИТМО: ФИО полностью и должность '
                        'руководителя практики, подразделение\n2) если сторонняя организация или по '
                        'месту работы: полное или краткое наименование организации, ИНН, '
                        'ФИО руководителя практики полностью, контактный номер телефона, корпоративный '
                        'адрес', parse_mode='html')
    await Profile.next()


@dp.message_handler(state=Profile.industrial_practice)
async def register_industrial_practice(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['industrial_practice'] = message.text

    await message.reply('Если <b>производственная</b> практика в сторонней организации (подписываю '
                        'договор и заявку на практику)\n1.Договор и заявка подписаны и сданы в Центр '
                        'карьеры\n2.Договор и заявка подписаны и НЕ сданы в Центр карьеры\n3.Договор '
                        'подписан и сдан в Центр карьеры\n4.Договор подписан и НЕ сдан в Центр карьеры'
                        '\n<b>отправьте номер выбранного варианта</b>'
                        '<b>Если вы не проходите производсвтенную практику в сторонней организации, напишите "-"</b>',
                        parse_mode='html')
    await Profile.next()


@dp.message_handler(state=Profile.other_industrial_practice)
async def register_other_industrial_practice(message: types.Message, state: FSMContext) -> None:
    if message.text == '1':
        dataMessage = 'Договор и заявка подписаны и сданы в Центр карьеры'
    elif message.text == '2':
        dataMessage = 'Договор и заявка подписаны и НЕ сданы в Центр карьеры'
    elif message.text == '3':
        dataMessage = 'Договор подписан и сдан в Центр карьеры'
    elif message.text == '4':
        dataMessage = 'Договор подписан и НЕ сдан в Центр карьеры'
    else:
        dataMessage = '-'

    async with state.proxy() as data:
        data['other_industrial_practice'] = dataMessage

    await message.reply('Если <b>производственная</b> практика по месту работы, если ещё не принесли - '
                        'выбираем вариант другое и пишем дату когда принесёте\n1.Заявление и копию '
                        'трудового договора принёс\n2.Другое\n'
                        '<b>Если вы не проходите производсвтенную практику по месту работы, напишите "-"</b>',
                        parse_mode='html')
    await Profile.next()


@dp.message_handler(state=Profile.work_industrial_practice)
async def register_work_industrial_practice(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['work_industrial_practice'] = message.text

    await message.reply('Если <b>производственная практика</b> в сторонней организации и подписана заявка, '
                        'Отправьте ссылку на заявку '
                        'заявку'
                        '<b>Если у вас нет заявки напишите "-"</b>', parse_mode='html')
    await Profile.next()


@dp.message_handler(state=Profile.other_industrial_practice_fileName)
async def register_other_industrial_practice_fileName(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['other_industrial_practice_fileName'] = message.document.file_id

    await message.reply('<b>Преддипломная практика</b>\n1.Руководитель ВКР уже есть,\n2.Руководителя '
                        'ВКР ещё нет'
                        '\n<b>отправьте номер выбранного варианта</b>', parse_mode='html')
    await Profile.next()


@dp.message_handler(state=Profile.undergraduate_practice)
async def register_undergraduate_practice(message: types.Message, state: FSMContext) -> None:
    if message.text == '1':
        dataMessage = 'Руководитель ВКР уже есть'
    elif message.text == '2':
        dataMessage = 'Руководителя ВКР ещё нет'
    else:
        dataMessage = 'not'

    async with state.proxy() as data:
        data['undergraduate_practice'] = dataMessage

        await loadDataToSheet(data)
    await message.reply('Поздравляю с регистрацией!')
    await state.finish()


# Популярные вопросы
@dp.message_handler(commands=['popular_questions'])
async def popular_questions(message: types.Message) -> None:
    global questions
    questions = await getQuestions()
    keyboard = InlineKeyboardMarkup()
    for question in questions:
        inlineButton = InlineKeyboardButton(question[1], callback_data=question[0])
        keyboard.add(inlineButton)
    await bot.send_message(message.from_user.id, text='Популярные вопросы: ', reply_markup=keyboard)


# Ответ на попрос
@dp.callback_query_handler()
async def callback_questions(callback: types.CallbackQuery):
    if callback.data.isdigit():
        idx = int(callback.data) - 1
        await callback.message.answer('Ответ: ' + questions[idx][2])


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)

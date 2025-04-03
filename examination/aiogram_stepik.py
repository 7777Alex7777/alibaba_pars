import requests
import time
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED, BaseFilter
from aiogram.types import Message, ContentType, ChatMemberUpdated
import random
import os
from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')


bot = Bot(token = bot_token)
dp = Dispatcher()

admin_ids = []

class IsAdmin(BaseFilter):
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids
    async def __call__(self, message: Message):
        return message.from_user.id in self.admin_ids


# Количество попыток, доступных пользователю в игре
ATTEMPTS = 5

# Словарь, в котором будут храниться данные пользователя
users = {}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


@dp.message(IsAdmin(admin_ids))
async def answer_if_admins_update(message: Message):
    await message.answer('Привет, админ!')
    print(message.model_dump_json(indent=3, exclude_none=True))


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    if message.from_user.username:
        await message.answer(
            'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
            'Чтобы получить правила игры и список доступных '
            'команд - отправьте команду /help'
        )
    else:
        await message.answer(
            'Привет, Сонечка, любимая, дорогая!\nДавайте сыграем в игру "Угадай число"?\n\n'
            'Чтобы получить правила игры и список доступных '
            'команд - отправьте команду /help'
        )
    # Если пользователь только запустил бота и его нет в словаре '
    # 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(
        f'Всего игр сыграно: '
        f'{users[message.from_user.id]["total_games"]}\n'
        f'Игр выиграно: {users[message.from_user.id]["wins"]}'
    )


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы итак с вами не играем. '
            'Может, сыграем разок?'
        )


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число больше')

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {users[message.from_user.id]["secret_number"]}'
                f'\n\nДавайте сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )

@dp.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def procees_user_blocked_bot(event: ChatMemberUpdated):
    print(event.from_user.id)




'''@dp.message(Command(commands=['start']))
async def   process_start_command(message: Message):
    await message.answer('Привет, бразе!')

@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Отправлю что пожелаешь')

@dp.message()
async def send_echo(message: Message):
    try:
        print(message.model_dump_json(indent=2, exclude_none=True))
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer('Взрыв машина')
'''


if __name__ == '__main__':
    dp.run_polling(bot)



'''api_url = 'https://api.telegram.org/bot'
token = '6674979922:AAH8v73BnU9xcOqt6vrTkLFDYcHz7oivFyA'
counter = 100
text = ''
offset = -2

while counter > 0:
    print(counter)
    response = requests.get(f'{api_url}{token}/getUpdates?offset={offset + 1}').json()

    if response['result']:
        for result in response['result']:
            chat_id = result['message']['from']['id']
            user_name = result['message']['from']['username']
            offset = result['update_id']
            if user_name == 'sonahoh':
                requests.get(f'{api_url}{token}/sendMessage?chat_id={chat_id}&text=Привет, Сонечка!!!!')
            else:
                requests.get(f'{api_url}{token}/sendMessage?chat_id={chat_id}&text=Сообщение получено, ежжи!')

    time.sleep(1)
    counter -= 1
'''

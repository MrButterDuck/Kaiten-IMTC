from telebot.async_telebot import AsyncTeleBot 
from telebot import types, asyncio_filters
from telebot.states import State, StatesGroup
from telebot.states.asyncio.context import StateContext
from telebot.asyncio_storage import StateMemoryStorage
from Kaiten import Kaiten

class MyStates(StatesGroup):
    kaiten_token = State()
    kaiten_domain = State()
    kaiten_space = State()
    kaiten_board = State()
    kaiten_column = State()
    sheet_url = State()
    set_timer = State()
    user_id = State()


class TelegramBot:
    def __init__(self, token, db) -> None:
        self.state_storage = StateMemoryStorage() 
        self.bot = AsyncTeleBot(token, state_storage=self.state_storage)
        self.db  = db
        self.kaiten = Kaiten(self.db.get_var("KAITEN_TOKEN"), self.db.get_var("KAITEN_DOMAIN"))
        self.user_id = self.db.get_var("USER_ID")

    def menu(self):
        @self.bot.message_handler(commands=['start','back', 'menu'])
        async def start(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/kaiten")
            btn2 = types.KeyboardButton("/google_sheets")
            btn3 = types.KeyboardButton("/timer")
            markup.add(btn1, btn2, btn3)
            await state.delete()
            await self.bot.send_message(message.from_user.id, f"Kaiten токен: {self.db.get_var("KAITEN_TOKEN")}\nKaiten домен: {self.db.get_var("KAITEN_DOMAIN")}\nKaiten таблица: {self.db.get_var("KAITEN_SPACE")}-{self.db.get_var("KAITEN_BOARD")}-{self.db.get_var("KAITEN_COLUMN")}\nGoogle Sheet: {self.db.get_var("GOOGLE_URL")}\nЧастота обновления: {self.db.get_var("UPDATE_TIMER")}\n\n=================\n\nСписок команд: \n/kaiten - настройки kaiten\n/google_sheets - настройки гугл таблиц\n/timer - настройки таймера", reply_markup=markup)
        
        @self.bot.message_handler(commands=['token', 'domain', 'space_id', 'board_id', 'column_id', 'url', 'set_timer'])
        async def set_var(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/back")
            markup.add(btn1)
            if message.text == "/token": 
                await state.set(MyStates.kaiten_token)
            if message.text == "/domain": 
                await state.set(MyStates.kaiten_domain)
            if message.text == "/space_id": 
                await state.set(MyStates.kaiten_space)
            if message.text == "/board_id": 
                await state.set(MyStates.kaiten_board)
            if message.text == "/column_id": 
                await state.set(MyStates.kaiten_column)
            if message.text == "/url": 
                await state.set(MyStates.sheet_url)
            if message.text == "/set_timer": 
                await state.set(MyStates.set_timer)
            if message.text == "/im_the_boss": 
                await state.set(MyStates.user_id)
            await self.bot.send_message(message.from_user.id, "Введите переменную", reply_markup=markup)

    def kaiten_module(self):
        @self.bot.message_handler(commands=['kaiten'])
        async def kaiten_menu(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/token")
            btn2 = types.KeyboardButton("/domain")
            btn3 = types.KeyboardButton("/board_list")
            btn4 = types.KeyboardButton("/space_id")
            btn5 = types.KeyboardButton("/board_id")
            btn6 = types.KeyboardButton("/column_id")
            btn7 = types.KeyboardButton("/back")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
            await self.bot.send_message(message.from_user.id, "Получить api можно здесь: \nhttps://developers.kaiten.ru", reply_markup=markup)


        @self.bot.message_handler(state=MyStates.kaiten_token)
        async def kaiten_token(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/menu")
            markup.add(btn1)
            await state.delete()
            self.db.add_var('KAITEN_TOKEN', message.text)
            self.update_kaiten()
            await self.bot.send_message(message.from_user.id, "Токен установлен", reply_markup=markup)

        @self.bot.message_handler(state=MyStates.kaiten_domain)
        async def kaiten_domain(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/menu")
            markup.add(btn1)
            await state.delete()
            self.db.add_var('KAITEN_DOMAIN', message.text)
            self.update_kaiten()
            await self.bot.send_message(message.from_user.id, "Домен установлен", reply_markup=markup)

        @self.bot.message_handler(state=MyStates.kaiten_space)
        async def kaiten_space(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/menu")
            markup.add(btn1)
            await state.delete()
            self.db.add_var('KAITEN_SPACE', message.text)
            await self.bot.send_message(message.from_user.id, "ID пространства установлен", reply_markup=markup)

        @self.bot.message_handler(state=MyStates.kaiten_board)
        async def kaiten_board(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/menu")
            markup.add(btn1)
            await state.delete()
            self.db.add_var('KAITEN_BOARD', message.text)
            await self.bot.send_message(message.from_user.id, "ID таблицы установлен", reply_markup=markup)

        @self.bot.message_handler(state=MyStates.kaiten_column)
        async def kaiten_column(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/menu")
            markup.add(btn1)
            await state.delete()
            self.db.add_var('KAITEN_COLUMN', message.text)
            await self.bot.send_message(message.from_user.id, "ID колоны установлен", reply_markup=markup)

        @self.bot.message_handler(commands=['board_list'])
        async def kaiten_list(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/menu")
            markup.add(btn1)
            await self.bot.send_message(message.from_user.id, "Запрос обрабатывается")
            connection = await self.kaiten.check_conntection()
            if connection:
                resp = await self.kaiten.get_all_boards()
                msg = ""
                for sp in resp:
                    msg += f'Пространство: {sp[0][1]} - {str(sp[0][0])}\n'
                    if sp[1]:
                        for brd in sp[1]:
                            msg += f'-+- Таблица: {brd[1]} - {str(brd[0])}\n'
                            if brd[1]:
                                for clmn in brd[2]:
                                    msg += f'-+- -+- Колонка: {clmn[1]} - {str(clmn[0])}\n'
                await self.bot.send_message(message.from_user.id, msg+'\n\nЗапомните нужные id и впишите, используая команды /space_id, /board_id и /column_id', reply_markup=markup)
            else:
                await self.bot.send_message(message.from_user.id, "Ошибка в подключении к Kaiten")

    def update_kaiten(self):
        self.kaiten = Kaiten(self.db.get_var("KAITEN_TOKEN"), self.db.get_var("KAITEN_DOMAIN"))
        return 
    
    def sheet_module(self):
        @self.bot.message_handler(commands=['google_sheets'])
        async def sheet_menu(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/url")
            btn7 = types.KeyboardButton("/back")
            markup.add(btn1, btn7)
            await self.bot.send_message(message.from_user.id, "Для работы необходима ссылка на табблицу, с которой будут браться данные\n\nУстановите ее с помощью команды /url", reply_markup=markup)

        @self.bot.message_handler(state=MyStates.sheet_url)
        async def sheet_url(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/menu")
            markup.add(btn1)
            await state.delete()
            self.db.add_var('GOOGLE_URL', message.text)
            await self.bot.send_message(message.from_user.id, "URL Google таблицы установлен", reply_markup=markup)

    def timer_module(self):
        @self.bot.message_handler(commands=['timer'])
        async def timer_menu(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/set_timer")
            btn7 = types.KeyboardButton("/back")
            markup.add(btn1, btn7)
            await self.bot.send_message(message.from_user.id, "Установка частоты обновления таблицы: \n/set_timer - установить частоту обновления в минутах(число меньше и равное 0 - отключить обновление)\n/im_the_boss - установка вас для уведомлений", reply_markup=markup)

        @self.bot.message_handler(state=MyStates.set_timer)
        async def set_timer(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/menu")
            markup.add(btn1)
            await state.delete()
            try:
                self.db.add_var('UPDATE_TIMER', int(message.text))
                await self.bot.send_message(message.from_user.id, "Частота обновления установлена", reply_markup=markup)
            except ValueError:
                await self.bot.send_message(message.from_user.id, "Введена не цифра, отмена команды", reply_markup=markup)

        @self.bot.message_handler(commands=['im_the_boss'])
        async def sheet_url(message: types.Message, state: StateContext):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/menu")
            markup.add(btn1)
            await state.delete()
            self.db.add_var('USER_ID', message.from_user.id)
            self.user_id =  message.from_user.id
            await self.bot.send_message(message.from_user.id, "Часть команды, часть корабля!", reply_markup=markup)

    async def notification(self, message):
        if self.user_id:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("/menu")
            markup.add(btn1)
            await self.bot.send_message(self.user_id, "Добавлена новая таска!\n\n=============\n\n"+message, reply_markup=markup)

    async def run(self, interval = 0):
        self.bot.add_custom_filter(asyncio_filters.StateFilter(self.bot))
        from telebot.states.asyncio.middleware import StateMiddleware
        self.bot.setup_middleware(StateMiddleware(self.bot))
        self.menu()
        self.kaiten_module()
        self.sheet_module()
        self.timer_module()
        await self.bot.polling(none_stop=True, interval=interval)
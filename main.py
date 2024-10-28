from Kaiten import Kaiten
from googleSheet import GoogleSheet
from db import ConfigDatabase
from bot import TelegramBot
from datetime import datetime
import asyncio
from pathlib import Path

async def bot_start(bot):
    await bot.run()

async def updater(db, bot):
    last_update = datetime.now()
    delay = db.get_var("UPDATE_TIMER")
    global addedNewCard
    while True:
        if delay and int(delay) > 0:
            if (datetime.now() - last_update).seconds >= int(delay)*60:
                last_update_buffer = last_update
                last_update = datetime.now()
                if db.get_var("GOOGLE_URL"):
                    sheet = GoogleSheet(db.get_var("GOOGLE_URL"))
                    records = sheet.get_records()
                    last_record_time = records[-1]['Отметка времени']
                    if last_update_buffer < datetime.strptime(last_record_time, "%d.%m.%Y %H:%M:%S"):
                        message = await kaiten_card_creater(db, list(records[-1].values()))
                        print('added new task'+ datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
                        await bot.notification(message)
                delay = db.get_var("UPDATE_TIMER")
            await asyncio.sleep(10)
        else:
            await asyncio.sleep(10)
            delay = db.get_var("UPDATE_TIMER")
            #print('no task '+ datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

async def kaiten_card_creater(db, record):
    kaiten = Kaiten(db.get_var("KAITEN_TOKEN"), db.get_var("KAITEN_DOMAIN"))
    desc = f'Контактные данные: {record[1]}\n\nПлатформа для публикации: {record[2]}\n\nКлючевые факты текста: {record[4]}\n\nМатериал заказчика: {record[5]}\n\nОписание изображения: {record[6]}\n\nРазмер изображения: {record[7]}' 
    kaiten.create_card(db.get_var("KAITEN_BOARD"),db.get_var("KAITEN_COLUMN"), record[3], desc, datetime.strftime(datetime.strptime(record[9], "%d.%m.%Y"), "%Y-%m-%d"))
    return f'Тема: {record[3]}\nДедлайн: {record[9]}\n\nКонтактные данные: {record[1]}\n\nПлатформа для публикации: {record[2]}\n\nКлючевые факты текста: {record[4]}\n\nМатериал заказчика: {record[5]}\n\nОписание изображения: {record[6]}\n\nРазмер изображения: {record[7]}' 

if __name__ == "__main__":
    if Path('googleAPI.json').is_file() and Path('bot_token.txt').is_file():
        db = ConfigDatabase("Config")
        token = Path('bot_token.txt').read_text()
        bot = TelegramBot(token, db)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(bot.run())
        loop.create_task(updater(db, bot))
        print('Bot is now running')
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
    else:
        print('Missing some files, cant start up')

from vkbottle.bot import Message, MessageEvent
from routes import labelers
from vkbottle import Bot
from routes.utils import *
from routes.db_connector import execute_select, execute_upd_ins
from dotenv import load_dotenv, find_dotenv
from art import tprint
import os
import datetime
import math
import time

load_dotenv(find_dotenv())
bot = Bot(os.getenv('TOKEN'))
admin_id = int(os.getenv('ADMIN_ID'))

tprint('LOADED', font='5lineoblique')



@bot.loop_wrapper.interval(seconds=5)
async def reminder():
    date_today = datetime.datetime.today().date()
    readable_time = int(time.mktime(time.strptime(f"{date_today}  10:00:00", "%Y-%m-%d %H:%M:%S")))
    weekday_today = datetime.date.today().weekday()
    if weekday_today == 6:
        return
    if weekday_today == 5 and math.floor(time.time()) >= readable_time:
        data = execute_select(
            f'''SELECT teacher_vk_id FROM `teachers_table` WHERE reminder = TRUE AND {readable_time + 43200} >= 
                        next_answer_time AND (class_name LIKE "1%" OR class_name LIKE "9%")''')
        for teacher in data:
            await bot.api.messages.send(peer_id=teacher[0].replace('id', ''),
                                        message="Не забудь написать кого сегодня нет!", random_id=0)
            execute_upd_ins(
                f'''UPDATE teachers_table SET next_answer_time = {generate()} WHERE teacher_vk_id = "{teacher[0]}"''')
    if weekday_today != 5 and math.floor(time.time()) >= readable_time:
        answer = execute_select(
            f'''SELECT teacher_vk_id FROM `teachers_table` WHERE reminder = TRUE AND {readable_time + 43200} >= 
               next_answer_time''')

        for teacher in answer:
            await bot.api.messages.send(peer_id=teacher[0].replace('id', ''),
                                        message="Не забудь написать кого сегодня нет!", random_id=0)
            execute_upd_ins(
                f'''UPDATE teachers_table SET next_answer_time = {generate()} WHERE teacher_vk_id = "{teacher[0]}"''')


@bot.on.private_message(text=['/репорт <ticket>', '.репорт <ticket>'])
async def report_handler(message: Message,  ticket):
    user_data = await bot.api.users.get(message.from_id)
    await bot.api.messages.send(random_id=0, peer_id=user_data[0].id, message="Ваше сообщение было отправлено")
    await bot.api.messages.send(random_id=0, peer_id=admin_id,
                                message=f'@id{admin_id}\n'
                                        f'У @id{user_data[0].id}({user_data[0].first_name}) возник вопрос: {ticket}')



@bot.on.private_message(text='/ad <announcement>')
async def announce_handler(message: Message, announcement):
    if message.from_id == admin_id:

        data = []

        try:
            answer = execute_select('''SELECT teacher_vk_id FROM teachers_table''')
            for i in answer:
                data.append(i[0].replace('id', ''))
            data.remove(str(admin_id))
            await bot.api.messages.send(random_id=0, peer_ids=data, message=f"📢 Объявление: {announcement}")
            await message.answer(message='Объявление было отправлено')
        except Exception as ad_error:
            await message.answer(message=ad_error)
            return


for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

if __name__ == "__main__":
    bot.run_forever()

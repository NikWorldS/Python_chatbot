from vkbottle.bot import BotLabeler, Message
import requests
from .utils import *
import sqlite3 as sq
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
admin_id = int(os.getenv('ADMIN_ID'))

bl = BotLabeler()


@bl.private_message(text=['/табель', ".табель"])
async def create_layout(event: Message):
    attach = event.attachments

    if attach.__len__() > 0:
        document = attach[0].doc

        if document is None:
            return

        if document.title.count(".") > 1:
            await event.answer("Произошла ошибка при определении файла, переименуйте файл так, чтобы в его названии не было точек.")
            return
        name, type_f = document.title.split(".")
        if type_f == 'xlsx':
            response = requests.get(document.url)
            with open(document.title, "wb") as f:
                f.write(response.content)
            create_temp = create_template(f"{document.title}")
            await event.answer(create_temp)
        elif type_f != 'xlsx':
            await event.answer(
                f'Возможно, отправленный файл не является табелем.\nЕсли ошибка повторяется, напишите @id{admin_id}')
    elif attach.__len__() == 0:
        await event.answer(f'К сообщению не прикреплён файл, прикрепи его, и напиши ту же команду в ОДНОМ сообщении')


@bl.private_message(text='. <missing>')
async def filling_tabel(event: Message, missing):
    if datetime.datetime.today().weekday() == 6:
        await event.answer(message="Сегодня воскресенье, ничего записываться не будет")
        return
    payers_dict = {}

    id_user = f"id{(await event.get_user(id)).get('id')}"

    conn = sq.connect("teachers_db.sqlite")
    cur = conn.cursor()

    (cur.execute(f'''SELECT class_name FROM `teachers_table` WHERE teacher_vk_id == "{id_user}"'''))
    class_n = cur.fetchone()[0].upper()

    missing = missing.split()

    payers = create_list_payers(class_n)
    for payer in payers:
        payers_dict[payer] = 'н'

    for person in payers_dict:
        if person in missing:
            payers_dict[person] = 'н'
        else:
            payers_dict[person] = 1

    cur.execute(f'''UPDATE teachers_table SET next_answer_time = {generate()} WHERE teacher_vk_id = "{id_user}"''')
    conn.commit()
    conn.close()
    values_list = list(payers_dict.values())
    filling_template(values_list, class_n)
    await event.answer(f"Сегодня {len(values_list) - values_list.count('н')} из {len(values_list)} платников")

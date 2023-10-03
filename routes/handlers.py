from vkbottle.bot import BotLabeler, Message
from .db_connector import execute_select, execute_upd_ins
from .keyboards import *
from .utils import *

bl = BotLabeler()


@bl.private_message(text='@id')
async def id_claimer(event: Message):
    id_person = await event.get_user(id)
    await event.answer(message=id_person)


@bl.private_message()
async def main_handler(event: Message):
    msg = event.text
    id_user = f"id{(await event.get_user(id)).get('id')}"
    if msg == "Старт" or msg == "Начать":
        await event.answer(message="Добро пожаловать в чат-бота! Эта инструкция поможет Вам разобраться со всеми функциями бота.\nВ самом начале Вы должны предоставить табель боту, отправив команду '.табель' и прикрепив к нему сам табель. Когда табель принят, Вы можете посмотреть список платников, которые прописаны в самом табеле. Для внесения данных об отсутствующих, Вы можете использовать команду '. (фамилия/ии)', после точки и фамилий должен быть только пробел. В конце недели Вы должны вывести табель командой 'Выведи табель', она находиться на главной странице бота. У бота также есть функция напоминалки - она оповещает Вас, если Вы не внесли данные об отсутствующих до 12 часов дня. Её можно отключить на странице настроек. Подробную информацию Вы можете получить на странице помощи.", keyboard=main_keyboard)
    elif msg == 'Список платников':
        try:
            class_name = execute_select(f'''SELECT class_name FROM teachers_table WHERE teacher_vk_id = "{id_user}"''')[0][0]
            payers = create_list_payers(class_name)
            data = f",\n-".join(payers)
            await event.answer(message=f"Список платников в Вашем классе:\n-{data}")
        except Exception as sq_class_error:
            await event.answer(message=f"Похоже, произошла ошибка. data: class_error |{sq_class_error}|")
    elif msg == "Настройки":
        try:
            remind = execute_select(f'''SELECT reminder FROM teachers_table WHERE teacher_vk_id = "{id_user}"''')[0][0]
            await event.answer(message="Вы на странице настроек бота",
                               keyboard=(settings_keyboard_true if remind is True else settings_keyboard_false))
        except Exception as sq_remind_error:
            await event.answer(message=f"Похоже, произошла ошибка. data: remind_error |{sq_remind_error}|")
    elif msg == "Назад":
        await event.answer(message="Вы на главной странице бота", keyboard=main_keyboard)
    elif msg == "Напоминалка":

        remind = execute_select(f'''SELECT reminder FROM teachers_table WHERE teacher_vk_id = "{id_user}"''')[0][0]

        if remind:
            execute_upd_ins(f'''UPDATE teachers_table SET reminder = 0 WHERE teacher_vk_id = "{id_user}"''')
            await event.answer(message=f"Напоминалка выключена", keyboard=settings_keyboard_false)
        else:
            execute_upd_ins(f'''UPDATE teachers_table SET reminder = 1 WHERE teacher_vk_id = "{id_user}"''')
            await event.answer(message=f"Напоминалка включена", keyboard=settings_keyboard_true)
    elif msg == "Помощь":
        await event.answer(message="Вы перешли на страницу помощи", keyboard=help_keyboard)
    elif msg == "Как добавить табель?":
        await event.answer(message="Для того, чтобы добавить табель, Вам необходимо отправить сообщение '.табель', и к этому же сообщению прикрепить файл с табелем, и бот Вам ответит. Если возникла проблема, можете написать репорт, как это сделать написано по кнопке 'Имеется вопрос?'")
    elif msg == "Как написать кого нет?":
        await event.answer(message="Для того, чтобы внести в табель информацию о том, кого нет, Вам необходимо написать команду '. (фамилия/ии), после точки и фамилий строго 1 пробел'")
    elif msg == "Как вывести табель?":
        await event.answer(message="Чтобы вывести табель, необходимо, чтобы сам табель (его макет) был сохранён в боте. Чтобы узнать, как это сделать, Вы можете нажать на кнопку 'Как добавить табель'. Если табель уже есть, то для того, чтобы вывести готовый табель, Вам необходимо нажать на зелёную кнопку 'Выведи табель', и табель отправиться Вам на почту, если не будет ошибок. ")
    elif msg == "Имеется вопрос?":
        await event.answer(message="Если у Вас имеется вопрос, идея или пожелание, Вы можете связаться с создателем по команде '.репорт (сообщение)'. По мере возможности, Вам ответят.")
    elif msg == "Команды":
        await event.answer(message="""Команда для заполнения табеля - '. (фамилия/ии)'. После точки и фамилий строго пробел.\nКоманда для добавления табеля - '.табель', и к этому сообщению необходимо прикрепить сам файл.""")

from aiogram import Bot, Dispatcher, types
import requests
from aiogram.fsm.state import StatesGroup, State


from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter, Command
import asyncio
import json

API_TOKEN = '7297121740:AAEhMu5huSooMGGQ-OpzrBSV0O6Vij8wedo'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class VacancyRequestStates(StatesGroup):
    keyword = State()
    count = State()
    ffrom  = State()

@dp.message(StateFilter(None), Command('vacancy'))
async def vacancy(message: types.Message, state: FSMContext):
    # r = requests.get('back/vacancy/get/')
    await message.reply("Привет! Пришли ключевое слово по которому мне надо найти вакансии:")
    await state.set_state(states.VacancyRequestStates.keyword)

@dp.message(states.VacancyRequestStates.keyword)
async def vacancy_keyword(message: types.Message, state: FSMContext):
    await state.update_data(keyword=message.text)
    await message.reply("А сколько вакансий вы хотите полусить?")
    await state.set_state(states.VacancyRequestStates.count)

@dp.message(states.VacancyRequestStates.count)
async def vacancy_count(message: types.Message, state: FSMContext):
    await state.update_data(count=message.text)
    await message.reply("И укажите id города:")
    await state.set_state(states.VacancyRequestStates.ffrom)

@dp.message(states.VacancyRequestStates.ffrom)
async def vacancy_from(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    headers = {
            'Content-Type': 'application/json; charset=utf-8',
    }
    r = requests.get(f"http://back:8000/vacancy/parse/{user_data['keyword']}/1/0", headers=headers)
    f = {
        'lol': 'lol'
    }
    await state.update_data(ffrom = 0)

    for ind, val in enumerate(r.json()["items"]):
        # await message.reply(v)
        
            name = val.get('name', 'Не указано')
            address = val.get('address', 'Не указано')
            url = val.get('url', 'Не указано')
            employer = val.get("employer", 'Не указано')
            employer_url = val.get("employer_url", 'Не указано')

            salo = val.get('salary_from', 'Не указано')
            if salo['to']:
                sal = f"{salo['from']} - {salo['to']} {salo['currency']}"
            else:
                sal = f"{salo['from']} {salo['currency']}"
            requirements = val.get('requirements', 'Не указано')['requirement']
            responsibilities = val.get('requirements', 'Не указано')['responsibility'].replace('highlighttext', 'b')
            experience = val.get('experience', 'Не указано')
            employment = val.get('employment', 'Не указано')
            await message.reply(f"""
<b>Название</b>: {name}
<b>Местоположение</b>: {address} 
<b>Работодатель</b>: <a href="{employer_url}">{employer}</a>
<b>Зарплата</b>: {sal}
<b>Требования</b>: {requirements}
<b>Обязанности</b>: {responsibilities}
<b>Опыт</b>: {experience}
<b>Занятость</b>: {employment}
<a href='{url}'>[URL]</a>
            """,parse_mode='HTML')
    await state.clear()

@dp.message(StateFilter(None), Command('continue'))
async def vacancy(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    await state.update_data(ffrom = int(user_data['ffrom'])+1)
    user_data = await state.get_data()
    headers = {
            'Content-Type': 'application/json; charset=utf-8',
    }
    r = requests.get(f"http://back:8000/vacancy/parse/{user_data['keyword']}/1/{user_data['ffrom']}/", headers=headers)
    await message.reply(str(r.content))
    for i in list(r.text):
        await message.reply(str(i))
        for val in i:
            await message.reply(str(val))
            name = val.get('name', 'Не указано')
            address = val.get('address', 'Не указано')
            url = val.get('url', 'Не указано')
            employer = val.get("employer", 'Не указано')
            employer_url = val.get("employer_url", 'Не указано')

            salo = val.get('salary_from', 'Не указано')
            if salo['to']:
                sal = f"{salo['from']} - {salo['to']} {salo['currency']}"
            else:
                sal = f"{salo['from']} {salo['currency']}"
            requirements = val.get('requirements', 'Не указано')['requirement']
            responsibilities = val.get('requirements', 'Не указано')['responsibility'].replace('highlighttext', 'b')
            experience = val.get('experience', 'Не указано')
            employment = val.get('employment', 'Не указано')
            await message.reply(f"""
<b>Название</b>: {name}
<b>Местоположение</b>: {address} 
<b>Работодатель</b>: <a href="{employer_url}">{employer}</a>
<b>Зарплата</b>: {sal}
<b>Требования</b>: {requirements}
<b>Обязанности</b>: {responsibilities}
<b>Опыт</b>: {experience}
<b>Занятость</b>: {employment}
<a href='{url}'>[URL]</a>
            """,parse_mode='HTML')
        await state.clear()
        # await message.reply("Привет! Пришли ключевое слово по которому мне надо найти вакансии:")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

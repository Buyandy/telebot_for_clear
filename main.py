from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import asyncio
from time import time
import json
import socket
import sys
from random import randint
import env
from datetime import date

API_TOKEN = '7553512028:AAGg8YpKYN2ho99MTxVfnRptB6CgdZ-bB8A'
bot = Bot(token=API_TOKEN)



class Tools:
    @staticmethod
    def get_days() -> int:
        print("Получения дня...")
        return int(int(time())/60/60/24)


    @staticmethod
    def get_data(path: str) -> dict:
        with open(path, "r") as file:
            return json.load(file)


    @staticmethod
    def save_data(path: str, data: dict) -> None:
        print("Сохраняю данные")
        with open(path, "w") as file:
            json.dump(data, file)
    

    @staticmethod
    def internet(host="8.8.8.8", port=53, timeout=3):
        print("Проверка доступа к инету...")
        """
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as ex:
            print(ex)
            return False
    
    @staticmethod
    def get_week_day():
        return date.today().weekday()
    
    

    




async def main():
    path: str = "data/data.json"
    tools: Tools = Tools()
    print("Получаю данные...")
    data: dict = tools.get_data(path)
    now_day: int = tools.get_days()
    #print(f"Получен дата: { now_day }")

    week_day: int = tools.get_week_day()
    (f"Получен день недели: { week_day }")

    


    #print("Сравниваю...")
    #print(f"{ now_day } and { data["now_day"] }")
    count_attemps: int = 0
    while count_attemps < 10:
        if tools.internet():
            if (week_day % 2) == 0:
                only_user = data["all_user"][int(week_day/2)]
                print(f"Выбран пользователь: { only_user }")

                
                fraze = env.get_fraza(only_user)
                await bot.send_message(data["chat_id"], fraze[randint(0, len(fraze)-1)])
                tools.save_data(path, data)
            else:
                print("Никто не моет полы)")
                await asyncio.sleep(1.0)
            break
        else:
            print("Ошибка! Нету доступа к инету!")
            for i in range(5):
                print(f"\rПовторный запрос будет через { 5-i } секунд! ({ count_attemps }/10)", end="")
                sys.stdout.flush()
                await asyncio.sleep(1.0)

            count_attemps += 1
    



if __name__ == '__main__':
    print("Запуск бота который определяет кто моет полы...")
    asyncio.run(main=main())
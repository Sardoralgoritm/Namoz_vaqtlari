from aiogram import Router, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from asyncio import run
from praytime import Prayers, Praytime
from userrouter import UserRouter

class MainBot:
    def __init__(self, tkn="6210753472:AAEZGgcz03vJA6pBiERuGf8qgDFsd4ZS47c") -> None:
        self.__dp = Dispatcher()
        self.__bot = Bot(token=tkn)
        self.prs = Prayers()
        self.prt = Praytime()
        self.__user = UserRouter(self.prt, self.prs)

    async def start(self):
        self.__user.register()
        self.__dp.include_router(self.__user.Urouter)
        try:
            await self.__dp.start_polling(self.__bot)
        except Exception as e:
            print(e)
            await self.__bot.session.close()

if __name__ == "__main__":
    mnb = MainBot()
    run(mnb.start())
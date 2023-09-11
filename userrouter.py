from aiogram import Router
from aiogram.types import Message, CallbackQuery
from praytime import Prayers, Praytime
from aiogram.filters.command import Command
from aiogram.filters.text import Text

class UserRouter:
    def __init__(self, pr_time:Praytime, prs:Prayers) -> None:
        self.__rout = Router()
        self.__pray_time = pr_time
        self.__prayers = prs

    async def start_message(self,msg:Message):
        welcome = f"""Assalomu alaykum {msg.from_user.full_name} Ibodatingiz har doim qabul bulsin """
        await msg.answer(text=welcome, reply_markup=self.__pray_time.get_regions())

    async def click_to_regions(self,clb:CallbackQuery):
        c_data = clb.data
        c_data = c_data.split(":")[1]
        html = self.__pray_time.get_request(c_data)
        if html == 404:
            await clb.answer(text="Afsuski ayni vaqtda qisqa muddatli texnik nosozlik mavjud", show_alert=True)

        elif html == "Cannot Finded your region!!!":
            await clb.answer(text="Afsuski ayni vaqtda viloyat topilmadi")

        else:
            self.__prayers.Content = html
            s = f"{c_data} viloyat bo'yicha namoz vaqtlari:"
            await clb.message.answer(text=s, reply_markup=self.__prayers.get_keyboards())
            await clb.answer(text="Ma'lumotlar sizga taqdim etildi")

    def register(self):
        
        self.__rout.message.register(self.start_message, Command("start"))
        self.__rout.callback_query.register(self.click_to_regions, Text(startswith="region"))

    @property
    def Urouter(self):
        return self.__rout
    
    # bu menisd
    
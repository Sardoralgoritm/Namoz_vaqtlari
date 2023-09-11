from requests import get, post, RequestException
from bs4 import BeautifulSoup
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

class Praytime:
    def __init__(self) -> None:
        self.__id_region = {
            "Andijon": "17",
            "Buxoro": "34",
            "Farg'ona": "77",
            "Jizzax": "107",
            "Xorazm": "101",
            "Namangan": "149",
            "Navoiy": "136",
            "Qashqadaryo": "121",
            "Samarqand": "47",
            "Sirdaryo": "73",
            "Surxondaryo": "162",
            "Toshkent": "1"
        }
        self.__url = "https://praytime.uz/"

    def get_regions(self):
        kbs = InlineKeyboardBuilder()
        for ks in self.__id_region.keys():
            kbs.add(InlineKeyboardButton(text=ks,callback_data="region:"+ks))
        kbs.adjust(4,4,4)
        return kbs.as_markup()

    def get_request(self,vlt:str):
        if vlt in self.__id_region.keys():
            data = {
                "region_id":self.__id_region[vlt]
            }
            ans = get(self.__url, params=data)
            if ans.status_code == 200:
                return ans.text
            else:
                return ans.status_code
        else:
            return "Cannot Finded your region!!!"
        

class Prayers:
    def __init__(self,html="") -> None:
        self.html = html
        self.dct = {
            "Tong":None,
            "Quyosh":None,
            "Peshin":None,
            "Asr":None,
            "Shom":None,
            "Xufton":None
        }
    
    @property
    def Content(self):
        return self.html
    
    @Content.setter
    def Content(self,vl:str):
        self.html = vl

    def __get_data(self):
        pry = BeautifulSoup(self.html, "html.parser")
        all_p = pry.find_all("div",class_ = "prayer-times")
        for el in all_p:
            sp = el.text.split("\n")
            if len(sp) != 5:
                self.dct[sp[1]] = sp[2]
            else:
                self.dct[sp[3]] = (sp[1],sp[2])

    def get_keyboards(self):
        self.__get_data()
        kbs = InlineKeyboardBuilder()
        for dd in self.dct.keys():
            str = ""
            if type(self.dct[dd]) != tuple:
                str = dd + "\n" + self.dct[dd]
            else:
                tp = self.dct[dd]
                str = dd + "✅" + "\n" + tp[0] + "\n" + tp[1]
            kbs.add(InlineKeyboardButton(text=str,callback_data="time:"+dd))
        kbs.adjust(1,1,1,1,1)
        return kbs.as_markup()
    
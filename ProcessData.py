from collections import Counter
import json
from list_conditions import list_conditions


class ProcessData:

    def __init__(self):
        self.list_conditions = list_conditions
        self.rare_floats = self.open_json('rare_floats.json')
        self.guns_id = []

    # открыть json
    @staticmethod
    def open_json(name_file: str) -> dict:
        with open(name_file) as file:
            file_content = file.read()
            content = json.loads(file_content)
        return content

    @staticmethod
    def write_json(name_file, data):
        with open(name_file, 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    # Проверка условий
    @staticmethod
    def verify_conditions(list_conditions_: list, checked_obj: dict) -> bool:
        for dict_condition in list_conditions_:
            if all([checked_obj['count_same_stickers'] == dict_condition['count_same_stickers'],
                    checked_obj['price_stickers'] >= dict_condition['price_stickers'],
                    checked_obj['self_price'] < checked_obj['suggested_price'],
                    checked_obj['self_price'] < dict_condition['self_price']
                    ]):
                return True
        return False

    # Сформировать строку для отправки в телеграм
    @staticmethod
    def formed_telegram_message(item: dict, rare_float=False) -> str:
        name = item.get('name')
        gun_float = item.get('gun_float')
        self_price = item.get('self_price')
        sugg_price = item.get('suggested_price')
        stickers = item.get('stickers')
        price_stickers = item.get('price_stickers')
        screenshot = str(item.get('screenshot'))
        count_same_stickers = item.get('count_same_stickers')
        link = f"{item.get('linkid')}"
        if rare_float:
            return f'#rarefloat \n #{count_same_stickers}\n {name} \n Флоат: {gun_float} \n Цена оружия: {self_price}$ \n средняя цена оружия: {sugg_price} \n \n Стикеры: {stickers} \n \n Общая цена стикеров: {price_stickers}$ \n\n Скриншот: {screenshot} \n\n ссылка: {link}'
        return f'#{count_same_stickers} \n {name} \n Флоат: {gun_float} \n Цена оружия: {self_price}$ \n средняя цена оружия: {sugg_price} \n \n Стикеры: {stickers} \n \n Общая цена стикеров: {price_stickers}$ \n\n Скриншот: {screenshot} \n\n ссылка: {link}'

    # получить суммарную стоимость стикеров на скине
    def get_sum_stickers(self, gun_info: dict) -> float:
        steam_price_stickers = self.open_json('price_stickers.json')
        sum_price_stickers = 0

        for sticker in gun_info.get('stickers'):
            if sticker != 'NoSticker' and steam_price_stickers.get('Sticker | ' + sticker):
                price_sticker = steam_price_stickers.get('Sticker | ' + sticker)
                sum_price_stickers += price_sticker

        return round(sum_price_stickers, 2)

    # Возвратить модифицрованный словарь с данными для проверки в verify_conditions
    def modified_dict(self, item: dict) -> dict:
        name = item.get('name')
        gun_float = item.get('gun_float')
        stickers = item.get('stickers')
        price_stickers = self.get_sum_stickers(item)
        count_same_stickers = max(Counter(stickers).values())
        inspect_in_game = str(item.get('rungame'))
        screenshot = f'https://market.swap.gg/screenshot?inspectLink={inspect_in_game}'
        link = f"https://dmarket.com/ingame-items/item-list/csgo-skins?userOfferId={item.get('linkid')}"
        self_price = item.get('price')
        suggested_price = item.get('suggestedPrice')

        return {'name': name, 'gun_float': gun_float, 'stickers': stickers, 'price_stickers': price_stickers,
                'count_same_stickers': count_same_stickers, 'screenshot': screenshot,
                'linkid': link, 'self_price': self_price, 'suggested_price': suggested_price
                }

    # проверка на редкий флоат
    def is_rare_float(self, item: dict) -> bool:
        name = item.get('name')
        try:
            gun_float = float(item.get('gun_float'))
        except Exception:
            return False
        if self.rare_floats.get(name) is None:
            return False
        rare_float = float(self.rare_floats.get(name).get('float'))
        if gun_float <= rare_float:
            # and item['self_price'] < item['suggested_price']:
            return True
        return False

    def send_to_telegram(self, guns_info, _bot):
        bot = _bot
        id_channel = '@dmparser152'
        rare_class_id = list(self.open_json('rare_classid.json'))
        for gun_info in guns_info:
            if gun_info.get('classId') in rare_class_id:
                continue
            rare_class_id.append(gun_info.get('classId'))
            self.write_json('rare_classid.json', rare_class_id)

            gun_info = self.modified_dict(gun_info)
            if self.verify_conditions(self.list_conditions, gun_info):
                bot.send_message(id_channel, text=self.formed_telegram_message(gun_info))
                # print(self.formed_telegram_message(gun_info))

            elif self.is_rare_float(gun_info):
                bot.send_message(id_channel, text=self.formed_telegram_message(gun_info, rare_float=True))
                # print(self.formed_telegram_message(gun_info, rare_float=True))

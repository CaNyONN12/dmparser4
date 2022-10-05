import requests


class CollectData:
    def __init__(self):
        self.__dm_url = 'https://api.dmarket.com/exchange/v1/market/items?side=market&orderBy=updated&orderDir=desc&title=&priceFrom=2&priceTo=1540&treeFilters=exterior%5B%5D=factory%20new,exterior%5B%5D=minimal%20wear,exterior%5B%5D=field-tested,exterior%5B%5D=well-worn,exterior%5B%5D=battle-scarred,category_1%5B%5D=not_souvenir&gameId=a8db&types=dmarket&cursor=&limit=100&currency=USD'
        self.__raw_guns_info = []
        self.__guns_id = []

    # Получить список стикеров предмета
    @staticmethod
    def __get_gun_stickers(item):
        stickers_info = item.get('extra').get('stickers')
        gun_stickers = []
        if stickers_info:
            for sticker in stickers_info:
                gun_stickers.append(sticker.get('name'))
        else:
            gun_stickers.append('NoSticker')
        return gun_stickers

    # добавить в список gun_info словарь содержащий информацию о предмете
    def __add_gun_info(self, item, gun_stickers):
        self.__raw_guns_info.append({
            'name': item.get('title'),
            'gun_float': item.get('extra').get('floatValue'),
            "linkid": item.get('extra').get('linkid'),
            'stickers': gun_stickers,
            'rungame': item.get('extra').get('inspectInGame'),
            'price': (float(item.get('price').get('USD')) / 100),
            'suggestedPrice': (float(item.get('suggestedPrice').get('USD')) / 100),
            'classId': item.get('classId')
        })
        self.__guns_id.append(item.get('classId'))

    # Собрать данные о предмете для обработки
    def collect_data(self):
        proxies = {
            "http": f"http://{'rmLcmR'}:{'vB5BrN'}@{'104.227.96.242:9890'}"
        }
        request = requests.get(url=self.__dm_url, proxies=proxies)
        data = request.json()
        items = data.get('objects')

        for item in items:
            gun_stickers = self.__get_gun_stickers(item)
            class_id = item.get('classId')
            if class_id not in self.__guns_id:
                self.__add_gun_info(item, gun_stickers)
        return self.__raw_guns_info

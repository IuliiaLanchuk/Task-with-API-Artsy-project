import requests
import json

client_id = '971834e4d02086bf1fdc'
client_secret = '579309c635090ee89c60da9d7693665c'

# инициируем запрос на получение токена
r = requests.post("https://api.artsy.net/api/tokens/xapp_token",
                  data={
                      "client_id": client_id,
                      "client_secret": client_secret
                  })

# разбираем ответ сервера
j = json.loads(r.text)

# # достаем токен
token = j["token"]

# создаем заголовок, содержащий наш токен
headers = {"X-Xapp-Token": token}

di = {} # cоздаем словарь, куда будем записывать имя и год рождения артистов. Например, id = 52f16a0e8b3b81a5b3000022
# id.txt где хранятся id артистов. Дальше мы будем добавлять id в url и получать json и вытягивать оттуда данные
with open('id.txt', 'r') as f:
    for line in f:
        id = str(line.rstrip())
        url = "https://api.artsy.net/api/artists/"
        result = requests.get(url+id, headers=headers)
        result.encoding = 'utf-8'
        data = result.json()
        # print(data)
        birthday = data['birthday']
        name = data["sortable_name"]
        di[name] = birthday

# сортировка полученных годов рождения и имен
di_list = list(di.items())
di_list.sort(key=lambda i: (i[1], i[0]))  # сортируется сначала по году, потом по имени

# если хотим записать результат в файл
with open('result.txt', 'w', encoding="UTF-8") as d:
    for i in di_list:
        # print(i[0], ':', i[1])
        d.write(i[0])
        d.write('\n')

# получим список имен отсортированный по дням рождения. А если дни рождения совпадают, то имена отсортированы по алфавиту
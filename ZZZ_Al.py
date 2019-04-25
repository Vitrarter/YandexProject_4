from flask import Flask, request
import logging
import json

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

sessionStorage = {}
ans = []


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    # Отправляем request.json и response в функцию handle_dialog.
    # Она сформирует оставшиеся поля JSON, которые отвечают
    # непосредственно за ведение диалога
    handle_dialog(request.json, response)

    logging.info('Response: %r', request.json)

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response)


def handle_dialog(req, res):
    global ans
    user_id = req['session']['user_id']  # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        # созда\м словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'first_name': None,
            'suggests': [
                "Мужигу",
                "Бабе",
                "Взрослому",
                "Ребенку",
                "Бытовой",
                "Досуг",
                "Для одного",
                "Для компании",
                "Техника",
                "Электроприборы",
                "от 2000 до 5000",
                "до 2000"
            ]
        }
        return

    if len(ans) == 0:
        res['response']['text'] = 'Кому вы хотите подарить подарок?'
    if 'мужиг' in req['request']['original_utterance'].lower() or 'мужчин' in req['request'][
        'original_utterance'].lower() \
            or 'пацан' in req['request']['original_utterance'].lower() or 'парн' in req['request'][
        'original_utterance'].lower() \
            or 'мальчик' in req['request']['original_utterance'].lower() or 'сын' in req['request'][
        'original_utterance'].lower():
        res['response']['text'] = 'Сколько ему лет?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(1)
        return



    elif 'баб' in req['request']['original_utterance'].lower() or 'женщин' in req['request'][
        'original_utterance'].lower() \
 \
            or 'феминистк' in req['request']['original_utterance'].lower() or 'девушк' in req['request'][
        'original_utterance'].lower() \
 \
            or 'девочк' in req['request']['original_utterance'].lower() or 'дочк' in req['request'][
        'original_utterance'].lower():
        res['response']['text'] = 'Сколько ей лет?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(0)
        return

    if 'стар' in req['request']['original_utterance'].lower() or 'пожил' in req['request']['original_utterance'].lower() \
            or 'взросл' in req['request']['original_utterance'].lower():
        res['response']['text'] = 'Какой тип товара вам подходит больше всего: бытовой или для дома?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(1)
        return


    elif 'молод' in req['request']['original_utterance'].lower() or 'ребёнк' in req['request'][
        'original_utterance'].lower() \
 \
            or 'ребёнок' in req['request']['original_utterance'].lower():
        res['response']['text'] = 'Какой тип товара вам подходит больше всего: бытовой или для дома?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(0)
        return

    if 'бытов' in req['request']['original_utterance'].lower():
        res['response']['text'] = 'Какой тип товара вам подходит больше всего: техника или электроприборы?'
        res['response']['buttons'] = get_suggests(user_id)
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(1)
        return


    elif 'досуг' in req['request']['original_utterance'].lower():
        res['response']['text'] = 'Какой тип товара вам подходит больше всего: для одного или для компании?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(0)
        return

    if 'техник' in req['request']['original_utterance'].lower():
        res['response']['text'] = 'Какой стоимости должен быть подарок?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(1)
        return


    elif 'электроприбор' in req['request']['original_utterance'].lower():
        res['response']['text'] = 'Какой стоимости должен быть подарок?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(0)
        return

    if 'для одного' in req['request']['original_utterance'].lower():
        res['response']['text'] = 'Какой стоимости должен быть подарок?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(1)
        return


    elif 'для компан' in req['request']['original_utterance'].lower():
        res['response']['text'] = 'Какой стоимости должен быть подарок?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(0)
        return

    if req['request']['original_utterance'].lower() in [
        'до 2000',
        '< 2000'
    ]:
        ans.append(1)
        res['response']['text'] = 'Вот что удалось подобрать!'
        res['response']['end_session'] = True
        res['response']['buttons'] = get_suggests(user_id)
        return

    elif req['request']['original_utterance'].lower() in [
        'от 2000 до 5000',
    ]:
        ans.append(0)
        res['response']['text'] = 'Вот что удалось подобрать!'
        res['response']['end_session'] = True
        res['response']['buttons'] = get_suggests(user_id)
        return

    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][2:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        if (ans[1] == 0 and ans[2] == 1):
            suggests.append({
                "title": "Ничего не удалось найти, но вы можете спросить у этого человека",
                "url": "https://m.vk.com/id242062417",
                "hide": True
            })
        elif ans[2] == 0:
            if ans[3] == 1:
                suggests.append({
                    "title": "Перети",
                    "url": "https://zak-zak.ru/products/nastolnaya-igra-manchkin-kvest-4-e-rus-izd",
                    "hide": True
                })
            elif ans[1] == 1:
                suggests.append({
                    "title": "Перети",
                    "url": "https://mtgtrade.net/store/",
                    "hide": True
                })
            else:
                suggests.append({
                    "title": "Перети",
                    "url": "https://zak-zak.ru/products/nastolnaya-igra-bashnya-skvirl",
                    "hide": True
                })
        elif ans[3] == 1:
            if ans[0] == 0:
                if ans[4] == 0:
                    suggests.append({
                        "title": "Перети",
                        "url": "https://market.yandex.ru/product--multivarka-redmond-rmk-m452/1723079328?show-uid=15562152959601729143716003&nid=54951&context=search",
                        "hide": True
                    })
                else:
                    suggests.append({
                        "title": "Перети",
                        "url": "https://market.yandex.ru/product--chainik-bosch-twk-3a011-3a013-3a014-3a017/8480393?show-uid=15562153850616723237016005&nid=54967&context=search",
                        "hide": True
                    })
            else:
                if ans[4] == 0:
                    suggests.append({
                        "title": "Перети",
                        "url": "https://market.yandex.ru/product--akusticheskaia-sistema-show-tc-1240/272668174?show-uid=15562155887456643917616070&nid=56153&context=search",
                        "hide": True
                    })
                else:
                    suggests.append({
                        "title": "Перети",
                        "url": "https://market.yandex.ru/product--akusticheskaia-sistema-cvgaudio-odf3t/359616098?show-uid=15562154779802586324816023&nid=56153&context=search",
                        "hide": True
                    })
        else:
            if ans[4] == 0:
                suggests.append({
                    "title": "Перети",
                    "url": "https://market.yandex.ru/product--naushniki-defender-accord-185/13599722?show-uid=15562160824423441632116002&nid=56179&pricefrom=1000&context=search",
                    "hide": True
                })
            else:
                suggests.append({
                    "title": "Перети",
                    "url": "https://market.yandex.ru/product--naushniki-jbl-t450bt/1713715931?show-uid=15562159872208239989116007&nid=56179&context=search",
                    "hide": True
                })
    return suggests


if __name__ == '__main__':
    app.run()

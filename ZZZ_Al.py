from flask import Flask, request
import logging
import json

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

sessionStorage = {}
ans = []


@app.route('/post', methods=['POST'])
def main():
    global ans
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
    if req['request']['original_utterance'].lower() in [
        'мужигу',
        'мужчине',
        'пацану',
        'парню',
        'мальчику',
        'сыну'
    ]:
        res['response']['text'] = 'Сколько ему лет?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(1)
        return


    elif req['request']['original_utterance'].lower() in [
        'бабе',
        'женщине',
        'феминистке',
        'девушке',
        'девочке',
        'дочке'
    ]:
        res['response']['text'] = 'Сколько ей лет?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(0)
        return


    if req['request']['original_utterance'].lower() in [
        'старая',
        'пожилая',
        'взрослая',
        'старый',
        'пожиой',
        'взрослый'
    ]:
        res['response']['text'] = 'Какой тип товара вам подходит больше всего?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(1)
        return

    elif req['request']['original_utterance'].lower() in [
        'молодой',
        'молодая',
        'ребёнку'
    ]:
        res['response']['text'] = 'Какой тип товара вам подходит больше всего?'
        res['response']['buttons'] = get_suggests(user_id)
        ans.append(0)
        return

    if len(ans) == 2:
        if ans[1]:
            res['response']['text'] = 'Какой тип товара вам подходит больше всего?'
            res['response']['buttons'] = get_suggests(user_id)
            res['response']['buttons'] = get_suggests(user_id)
            ans.append(1)
            return

        else:
            res['response']['text'] = 'Какой тип товара вам подходит больше всего?'
            res['response']['buttons'] = get_suggests(user_id)
            ans.append(0)
            return

    elif len(ans) == 3:
        res['response']['text'] = 'Какой стоимости должен быть подарок?'
        res['response']['end_session'] = True
        return

    elif len(ans) == 4:
        if req['request']['original_utterance'].lower() in [
            'до 2000',
            '< 2000'
        ]:
            ans.append(1)
        else:
            ans.append(0)
        res['response']['text'] = 'Вот что удалось подобрать!'
        res['response']['end_session'] = True
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
        suggests.append({
            "title": "Перейти",
            "url": "https://m.vk.com/id242062417",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    app.run()
